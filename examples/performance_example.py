"""
MODULE: services/database/examples/performance_example.py
PURPOSE: Demonstrates how to use the database performance monitoring tools
CLASSES:
    - None
FUNCTIONS:
    - main: Entry point for the example
DEPENDENCIES:
    - services.database: For database operations
    - services.database.performance: For performance monitoring
    - time: For time manipulation
    - statistics: For statistical analysis

This module provides a practical example of using the database performance
monitoring tools to log and analyze query performance. It demonstrates how to 
use the QueryLogger and time_query decorator to monitor database operation
performance and identify slow queries.

Example usage:
```
python services/database/examples/performance_example.py
```
"""

import time
import statistics
from typing import Dict, Any, List, Optional
import random
from datetime import datetime, timedelta

# Import database components
from services.database import DBOperator
from services.database.performance import QueryLogger, time_query, QueryLogEntry

def run_example_queries(db: DBOperator, iterations: int = 5) -> None:
    """
    Run example queries to demonstrate performance monitoring.
    
    Args:
        db: Database operator
        iterations: Number of iterations to run for each query
    """
    print("\n=== Running Example Queries ===\n")
    
    # Example 1: Basic query
    print("1. Running basic query...")
    for i in range(iterations):
        # Add a small sleep to simulate varying network conditions
        time.sleep(random.uniform(0.01, 0.05))
        
        result = db.fetch_all("SELECT * FROM public.users LIMIT 10")
        print(f"   Iteration {i+1}: Retrieved {len(result)} rows")
    
    # Example 2: Query with a JOIN
    print("\n2. Running query with JOIN...")
    for i in range(iterations):
        # Add a small sleep to simulate varying network conditions
        time.sleep(random.uniform(0.02, 0.08))
        
        result = db.fetch_all("""
            SELECT u.*, p.title, p.content 
            FROM public.users u
            JOIN public.posts p ON u.id = p.user_id
            LIMIT 5
        """)
        print(f"   Iteration {i+1}: Retrieved {len(result)} rows")
    
    # Example 3: Query with GROUP BY
    print("\n3. Running query with GROUP BY...")
    for i in range(iterations):
        # Add a small sleep to simulate varying network conditions
        time.sleep(random.uniform(0.03, 0.1))
        
        result = db.fetch_all("""
            SELECT u.status, COUNT(*) as user_count
            FROM public.users u
            GROUP BY u.status
        """)
        print(f"   Iteration {i+1}: Retrieved {len(result)} rows")
    
    # Example 4: Slow query (simulated)
    print("\n4. Running slow query (simulated)...")
    for i in range(iterations):
        # Simulate a slow query with a longer sleep
        time.sleep(random.uniform(0.2, 0.4))
        
        result = db.fetch_all("""
            SELECT u.*, 
                   (SELECT COUNT(*) FROM public.posts WHERE user_id = u.id) as post_count,
                   (SELECT COUNT(*) FROM public.comments WHERE user_id = u.id) as comment_count
            FROM public.users u
            ORDER BY u.created_at DESC
            LIMIT 10
        """)
        print(f"   Iteration {i+1}: Retrieved {len(result)} rows")

@time_query
def decorated_example_query(db: DBOperator) -> List[Dict[str, Any]]:
    """
    Example function with time_query decorator.
    
    Args:
        db: Database operator
        
    Returns:
        List of query results
    """
    # Simulate query execution time
    time.sleep(random.uniform(0.05, 0.15))
    
    # Execute query
    return db.fetch_all("""
        SELECT u.*, 
               p.title as latest_post_title,
               p.created_at as latest_post_date
        FROM public.users u
        LEFT JOIN public.posts p ON u.id = p.user_id
        WHERE u.status = 'active'
        ORDER BY p.created_at DESC
        LIMIT 15
    """)

def analyze_logs(query_logger: QueryLogger) -> None:
    """
    Analyze query logs and print performance statistics.
    
    Args:
        query_logger: Query logger instance with collected logs
    """
    logs = query_logger.get_logs()
    
    print("\n=== Query Performance Analysis ===\n")
    
    print(f"Total queries logged: {len(logs)}")
    
    # Group logs by query type
    query_groups = {}
    for log in logs:
        query = log.sql.strip().split('\n')[0].strip()  # Get first line of query
        if query not in query_groups:
            query_groups[query] = []
        query_groups[query].append(log)
    
    print(f"\nUnique query types: {len(query_groups)}")
    
    # Calculate statistics for each query type
    print("\nQuery Performance by Type:")
    print("-" * 80)
    print(f"{'Query Type':<40} | {'Avg Time (ms)':<12} | {'Min (ms)':<10} | {'Max (ms)':<10} | {'Count':<5}")
    print("-" * 80)
    
    for query, logs in query_groups.items():
        query_display = (query[:37] + '...') if len(query) > 40 else query
        execution_times = [log.execution_time_ms for log in logs]
        avg_time = statistics.mean(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        count = len(logs)
        
        print(f"{query_display:<40} | {avg_time:<12.2f} | {min_time:<10.2f} | {max_time:<10.2f} | {count:<5}")
    
    # Identify slow queries (> 100ms)
    slow_logs = [log for log in logs if log.execution_time_ms > 100]
    
    print(f"\nSlow Queries (>100ms): {len(slow_logs)}")
    if slow_logs:
        print("-" * 80)
        print(f"{'Query':<50} | {'Time (ms)':<10} | {'Timestamp':<20}")
        print("-" * 80)
        
        for log in sorted(slow_logs, key=lambda x: x.execution_time_ms, reverse=True):
            query_display = (log.sql.split('\n')[0][:47] + '...') if len(log.sql.split('\n')[0]) > 50 else log.sql.split('\n')[0]
            timestamp = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{query_display:<50} | {log.execution_time_ms:<10.2f} | {timestamp:<20}")

def main() -> None:
    """
    Entry point for the database performance monitoring example.
    """
    print("\n=== Database Performance Monitoring Example ===\n")
    
    # Create a DBOperator with mock mode for this example
    print("1. Creating DBOperator in mock mode...")
    db = DBOperator(test_mode="mock")
    print("   DBOperator created successfully!")
    
    # Enable query logging
    print("\n2. Enabling query logging...")
    query_logger = QueryLogger()
    db.set_query_logger(query_logger)
    print("   Query logging enabled!")
    
    # Run example queries to collect performance data
    print("\n3. Running example queries to collect performance data...")
    run_example_queries(db)
    
    # Example with time_query decorator
    print("\n4. Running function with time_query decorator...")
    decorated_results = []
    for i in range(3):
        result = decorated_example_query(db)
        decorated_results.append(result)
        print(f"   Iteration {i+1}: Retrieved {len(result)} rows")
    
    # Analyze the logs
    print("\n5. Analyzing query logs...")
    analyze_logs(query_logger)
    
    # Export logs to CSV (example)
    print("\n6. Exporting logs to CSV...")
    csv_path = "query_performance_logs.csv"
    query_logger.export_to_csv(csv_path)
    print(f"   Logs exported to: {csv_path}")
    
    print("\n=== Example Complete ===\n")

if __name__ == "__main__":
    main() 