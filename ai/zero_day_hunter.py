# ai/zero_day_hunter.py
def generate_fuzz_payloads():
    return ["A"*100, "' OR 1=1--", "<script>", "%n%n%n"]

def fuzz_service(target, port=80):
    for payload in generate_fuzz_payloads():
        try:
            r = requests.get(f"http://{target}:{port}/?q={payload}", timeout=3)
            if "error" in r.text and "stack" in r.text:
                return f"🔥 Zero-day ditemukan: {target}:{port}"
        except:
            pass
    return None