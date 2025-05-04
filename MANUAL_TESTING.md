# Manual Testing Instructions for Chunking Optimization

## Test Setup
1. Ensure Python environment is active
2. Install requirements: `pip install -r requirements.txt`
3. Have test documents ready in `docs/` folder

## Test Cases

### 1. Verify Configurable Chunk Sizes
```bash
# Edit config.yaml and change:
chunk_size: 500  # Try different values (500, 1000, 1500)
chunk_overlap: 100  # Try different values (100, 200)

# Run the application
streamlit run src/main.py

# Verify in logs:
- DocumentLoader should show new chunk parameters
- Check chunk counts match expected based on document sizes
```

### 2. Test Document Processing
```bash
# Add a test document to docs/ folder
echo "Test content with about 2000 characters..." > docs/test.md

# Run and verify:
- Documents load without errors
- Chunk sizes in logs match config
- Retrieved chunks have correct overlap
```

### 3. Verify Backward Compatibility
```bash
# Restore default config:
chunk_size: 1000
chunk_overlap: 200

# Run and verify:
- System behaves exactly as before changes
- All existing functionality works
```

### 4. Edge Cases
- Test with empty documents
- Test with very small/large chunk sizes
- Verify error handling for invalid config values

## Expected Results
- Chunk sizes should match config exactly
- Overlap should never exceed chunk size
- System should handle all test cases without errors
