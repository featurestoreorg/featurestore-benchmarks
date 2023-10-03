package org.example;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import java.sql.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import static com.google.common.math.Quantiles.percentiles;

public class Main {

  static final String DB_URL = "jdbc:mysql://34.16.179.140:3306/javier?useSSL=false&allowPublicKeyRetrieval=true";
  static final String USER = "javier_meb10000";
  static final String PASS = "lYjeMNkQRBnpfDboUOpFCcoGsQpFwLsD";
  //
 // static final String DB_URL = "jdbc:mysql://34.79.76.124:3306/overstock?useSSL=false&allowPublicKeyRetrieval=true";
  //static final String USER = "overstock_meb10000";
 // static final String PASS = "YLNRJHsypODqNbgtgBleYQWttnpkeTRH"; 
  static final String QUERY = "select product_id, col_float_1, col_float_2,col_float_3,col_float_4,col_float_5," +
    "col_float_6,col_float_7,col_float_8,col_float_9,col_float_10,col_float_11,col_str_1, col_str_2, col_str_3, col_str_4, col_str_5, col_float_12, col_float_13, col_float_14, col_float_15, col_float_16, col_float_17, col_list_0, col_list_2  from products_1 where product_id in (%s)";

  public static class HikariCPDataSource {

    private static HikariConfig config = new HikariConfig();
    private static HikariDataSource ds;

    static {
      config.setJdbcUrl(DB_URL);
      config.setUsername(USER);
      config.setPassword(PASS);
      config.addDataSourceProperty("cachePrepStmts", "true");
      config.addDataSourceProperty("prepStmtCacheSize", "250");
      config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");
      ds = new HikariDataSource(config);
    }

    public static Connection getConnection() throws SQLException {
      return ds.getConnection();
    }

    private HikariCPDataSource() {
    }
  }

  public static List<String> getIdSamples(int maxId, int limit) {
    ArrayList<String> idPool = new ArrayList<String>(maxId + 1);
    for (int i = 0; i <= maxId; i++) {
      idPool.add(String.valueOf(i));
    }
    Collections.shuffle(idPool);
    return idPool.subList(0, limit);
  }

  public static long executeStatement(PreparedStatement stmt, int maxId, int limit) throws SQLException {
    List<String> ids = getIdSamples(maxId, limit);

    int i = 1;
    for (String id : ids) {
      stmt.setObject(i++, id);
    }

//    System.out.println(stmt.toString());

    stmt.setQueryTimeout(10);

    long startQuery = System.currentTimeMillis();
    ResultSet rs = stmt.executeQuery();
    while (rs.next()) {
    }
    long end = System.currentTimeMillis();
    return end - startQuery;
  }

  public static long[] executeNTimes(PreparedStatement stmt, int maxId, int limit, int times) throws SQLException {
    long[] executionTimes = new long[times];
    for (int i = 0; i < times; i++) {
      executionTimes[i] = executeStatement(stmt, maxId, limit);
    }
    return executionTimes;
  }

  public static void main(String[] args) throws SQLException {
    int limit = Integer.parseInt(args[0]);
    int warmups = Integer.parseInt(args[1]);
    int executions = Integer.parseInt(args[2]);
    int maxId = 1000;

    Connection conn = HikariCPDataSource.getConnection();

    StringBuilder stringBuilder = new StringBuilder();
    for (int i = 0; i < limit - 1; i++) {
      stringBuilder.append("?, ");
    }
    stringBuilder.append("?");

    PreparedStatement stmt = conn.prepareStatement(String.format(QUERY, stringBuilder.toString()));

    executeNTimes(stmt, maxId, limit, warmups);

    long[] executionTimes = executeNTimes(stmt, maxId, limit, executions);

    Map<Integer, Double> myPercentiles =
      percentiles().indexes(50, 90, 95, 99).compute(executionTimes);
    myPercentiles.forEach((k, v) -> System.out.println(("p" + k + ":" + v + "ms")));
  }
}
