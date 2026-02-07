import os
import lancedb
from fastembed import TextEmbedding
from typing import List, Dict, Any
import uuid
import time
import json

# Omni Swarm Memory (v0.7.1)
# Uses LanceDB + FastEmbed for local vector storage.

DB_PATH = os.path.expanduser("~/.omni/memory.lance")
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

class SwarmMemory:
    def __init__(self, table_name="shared_context"):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.db = lancedb.connect(DB_PATH)
        self.model = TextEmbedding(model_name=EMBEDDING_MODEL)
        self.table_name = table_name
        self.table = self._init_table()

    def _init_table(self):
        """Initialize or load the table."""
        try:
            if self.table_name in self.db.table_names():
                return self.db.open_table(self.table_name)
        except:
            pass
        return None

    def add(self, text: str, agent: str, metadata: Dict[str, Any] = {}):
        """Embed and store a memory fragment."""
        vector = list(self.model.embed([text]))[0]
        
        record = {
            "id": str(uuid.uuid4()),
            "vector": vector,
            "text": text,
            "agent": agent,
            "timestamp": time.time(),
            "metadata": json.dumps(metadata)
        }
        
        if self.table is None:
            self.table = self.db.create_table(self.table_name, data=[record])
        else:
            self.table.add([record])
            
        print(f"💾 Memory saved: {text[:30]}...")

    def search(self, query: str, limit=3):
        """Semantic search."""
        if self.table is None:
            return []
            
        # Embed query
        query_vec = list(self.model.embed([query]))[0]
        
        # Search
        results = self.table.search(query_vec).limit(limit).to_list()
        return results

    def wipe(self):
        """Clear memory."""
        try:
            if self.table_name in self.db.table_names():
                self.db.drop_table(self.table_name)
        except:
            pass
        self.table = None

if __name__ == "__main__":
    mem = SwarmMemory()
    mem.add("The user wants a dark mode dashboard.", "@roe/frontend")
    mem.add("The database schema uses UUIDs.", "@roe/backend")
    
    print("\n🔍 Searching for 'database'...")
    results = mem.search("database schema")
    for r in results:
        print(f" - {r['text']} (Agent: {r['agent']})")
