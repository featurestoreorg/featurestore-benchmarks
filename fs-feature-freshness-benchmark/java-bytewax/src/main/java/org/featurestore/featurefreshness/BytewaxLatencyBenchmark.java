package org.featurestore.featurefreshness;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.LongSummaryStatistics;
import java.util.Map;

import static com.google.common.math.Quantiles.percentiles;

/* Usage:
 *
 * export DB_URL="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_URL"
 * export USER="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_USER"
 * export PASS="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_PASSWORD"
 *
 * java -jar bytewaxlatencybenchmark-1.0-SNAPSHOT-jar-with-dependencies.jar BATCH_SIZE START_ID ROUNDS
 * BATCH_SIZE - Maximum number of ids to be fetched in one request. Default is 50.
 * START_ID - Id of the first record to be fetched. Default is 1.
 * ROUNDS - How many batches to fetch. Default is 100.
 */
public class BytewaxLatencyBenchmark {
  static final String DB_URL = System.getenv("DB_URL");
  static final String USER = System.getenv("USER");
  static final String PASS = System.getenv("PASS");
  static final String QUERY = "SELECT user_id, timestamp FROM clicks_1 WHERE user_id in (%s)";

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

  public static void main(String[] args) throws SQLException, InterruptedException {
    int batchSize = 50;
    int startId = 1;
    int rounds = 100;

    try {
      batchSize = Integer.parseInt(args[0]);
    } catch (ArrayIndexOutOfBoundsException e) {
      System.out.println("BATCH_SIZE not set. Assuming default 50.");
    }

    try {
      startId = Integer.parseInt(args[1]);
      if (startId < 1) {
        startId = 1;
        System.out.println("START_ID lower than 1. Assuming 1.");
      }
    } catch (ArrayIndexOutOfBoundsException e) {
      System.out.println("START_ID not set. Assuming default 1.");
    }

    try {
      rounds = Integer.parseInt(args[2]);
    } catch (ArrayIndexOutOfBoundsException e) {
      System.out.println("ROUNDS not set. Assuming default 100.");
    }

    StringBuilder stringBuilder = new StringBuilder();
    for (int i = 0; i < batchSize - 1; i++) {
      stringBuilder.append("?, ");
    }
    stringBuilder.append("?");

    Connection conn = HikariCPDataSource.getConnection();
    PreparedStatement stmt = conn.prepareStatement(String.format(QUERY, stringBuilder));

    int nextId = startId;
    for (int i = 1; i <= batchSize; i++) {
      stmt.setInt(i, nextId);
      nextId++;
    }

    long[] durations = new long[rounds];
    int round = 0;
    int largestId = startId - 1;
    String msg = "Waiting for the first batch with ids between %d and %d";
    System.out.println(String.format(msg, largestId + 1, largestId + batchSize));
    boolean printedStart = false;
    while (round < rounds) {
      ResultSet rs = stmt.executeQuery();
      long now = System.currentTimeMillis();

      int currentLargestId = 0;
      long timestamp = 0;
      while (rs.next()) {
        if (round == 0 && !printedStart) {
          System.out.println("Started receiving batches");
          printedStart = true;
        }
        if (rs.getInt("user_id") > currentLargestId) {
          currentLargestId = rs.getInt("user_id");
          timestamp = rs.getTimestamp("timestamp").getTime();
        }
      }

      if (largestId < currentLargestId) {
        long duration = now - timestamp;
        durations[round] = duration;
        round++;
        largestId = currentLargestId;

        nextId = currentLargestId + 1;
        for (int i = 1; i <= batchSize; i++) {
          stmt.setInt(i, nextId);
          nextId++;
        }
      } else {
        Thread.sleep(1);
      }
    }

    System.out.println(String.format("\nStatistics for %d rounds with batches of size up to %d:\n", rounds, batchSize));

    LongSummaryStatistics stat = Arrays.stream(durations).summaryStatistics();
    System.out.println(String.format("Minimum latency: %dms", stat.getMin()));
    System.out.println(String.format("Maximum latency: %dms", stat.getMax()));
    System.out.println(String.format("Average latency: %.0fms\n", stat.getAverage()));

    Map<Integer, Double> myPercentiles =
      percentiles().indexes(50, 90, 95, 99).compute(durations);
    myPercentiles.forEach((k, v) -> System.out.println(("p" + k + " latency: " + v + "ms")));
  }
}
