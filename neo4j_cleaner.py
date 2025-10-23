from neo4j import GraphDatabase

#initial parameters

DATA_PATH = "data/kaggle/events.csv"  
SAMPLE_MAX_SESSIONS = 200000  
MIN_SESSION_LENGTH = 2  
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "nahi1420")  
BATCH_SIZE = 5000  

def get_driver(uri=NEO4J_URI, auth=NEO4J_AUTH):
    return GraphDatabase.driver(uri, auth=auth, encrypted=False)
def clear_db_in_chunks(driver, chunk_size=5000):
    """
    Deletes all nodes and relationships from the database in memory-friendly chunks.
    This is an alternative to apoc.periodic.iterate when APOC is not installed.
    """
    print("Starting chunked database deletion...")
    driver.verify_connectivity()
    
    deleted_count = 0
    total_deleted = 0
    
    while True:
        # Cypher query to find and delete a small batch of nodes
        query = f"""
        MATCH (n) 
        WITH n LIMIT {chunk_size} 
        DETACH DELETE n 
        RETURN count(n) AS deleted
        """
        
        with driver.session() as session:
            result = session.run(query)
            deleted_count = result.single()["deleted"]
            total_deleted += deleted_count
            
        print(f"Deleted {deleted_count} nodes in chunk. Total deleted: {total_deleted}")
        
        # Stop the loop when fewer nodes than the chunk size were found (meaning we hit the end)
        if deleted_count < chunk_size:
            break
            
    print("\nDatabase successfully cleared!")
    return total_deleted

# --- EXECUTION ---
driver = get_driver()
clear_db_in_chunks(driver)
driver.close()