# genauth_app.py – GenAuth: AI Identity & Authorship Blockchain (Flask, Vercel)

from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time
import os
from uuid import uuid4

CHAIN_FILE = 'genauth_chain.json'
app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, artifact_id, agent_name, content_hash, fingerprint, purpose, signature, tags, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.artifact_id = artifact_id
        self.agent_name = agent_name
        self.content_hash = content_hash
        self.fingerprint = fingerprint
        self.purpose = purpose
        self.signature = signature
        self.tags = tags
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        return hashlib.sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

class GenAuthChain:
    difficulty = 4

    def __init__(self):
        self.queue = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return [Block(0, time.time(), "GENESIS", "System", "0", "0", "Initialization", "N/A", [], "0")]

    def last_block(self):
        return self.chain[-1]

    def submit_artifact(self, agent_name, content_hash, fingerprint, purpose, signature, tags):
        artifact_id = str(uuid4())
        self.queue.append({
            'artifact_id': artifact_id,
            'agent_name': agent_name,
            'content_hash': content_hash,
            'fingerprint': fingerprint,
            'purpose': purpose,
            'signature': signature,
            'tags': tags
        })
        return artifact_id

    def proof_of_work(self, block):
        block.nonce = 0
        hashed = block.compute_hash()
        while not hashed.startswith('0' * GenAuthChain.difficulty):
            block.nonce += 1
            hashed = block.compute_hash()
        return hashed

    def add_block(self, block, proof):
        if self.last_block().hash != block.previous_hash:
            return False
        if not proof.startswith('0' * GenAuthChain.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine_artifact(self):
        if not self.queue:
            return False
        data = self.queue.pop(0)
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            artifact_id=data['artifact_id'],
            agent_name=data['agent_name'],
            content_hash=data['content_hash'],
            fingerprint=data['fingerprint'],
            purpose=data['purpose'],
            signature=data['signature'],
            tags=data['tags'],
            previous_hash=self.last_block().hash
        )
        proof = self.proof_of_work(block)
        if self.add_block(block, proof):
            return block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([b.__dict__ for b in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            return [Block(**b) for b in json.load(f)]

chain = GenAuthChain()

@app.route('/')
def explorer():
    html = """
    <html><head><title>GenAuth Explorer</title><style>
    body { font-family: sans-serif; background: #f7f7f7; padding: 20px; }
    .block { background: white; padding: 15px; border-radius: 8px; margin: 10px 0; box-shadow: 0 0 6px rgba(0,0,0,0.1); }
    </style></head><body>
    <h1>🧾 GenAuth Chain – Authorship Verification</h1>
    {% for block in chain %}
    <div class="block">
        <h3>Block #{{ block.index }} – {{ block.agent_name }}</h3>
        <p><b>Artifact ID:</b> {{ block.artifact_id }}</p>
        <p><b>Content Hash:</b> {{ block.content_hash }}</p>
        <p><b>Fingerprint:</b> {{ block.fingerprint }}</p>
        <p><b>Purpose:</b> {{ block.purpose }}</p>
        <p><b>Signature:</b> {{ block.signature }}</p>
        <p><b>Tags:</b> {{ block.tags }}</p>
        <p><b>Hash:</b> {{ block.hash }}</p>
        <p><b>Previous Hash:</b> {{ block.previous_hash }}</p>
    </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, chain=chain.chain)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    required = ('agent_name', 'content_hash', 'fingerprint', 'purpose', 'signature', 'tags')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    artifact_id = chain.submit_artifact(
        data['agent_name'], data['content_hash'], data['fingerprint'],
        data['purpose'], data['signature'], data['tags']
    )
    return jsonify({'message': 'Artifact submitted', 'id': artifact_id})

@app.route('/mine')
def mine():
    index = chain.mine_artifact()
    return jsonify({'message': f'Block #{index} mined' if index is not False else 'No artifacts to mine'})

@app.route('/chain')
def full_chain():
    return jsonify([b.__dict__ for b in chain.chain])

app = app  # For Vercel compatibility
