from src.llm_client import safe_generate

sample_diff = """diff --git a/example.py b/example.py
index 123456..abcdef 100644
--- a/example.py
+++ b/example.py
@@ -1,3 +1,4 @@
-print("Hello World")
+print("Hello AI World")
"""

summary = safe_generate(sample_diff)
print(summary)
