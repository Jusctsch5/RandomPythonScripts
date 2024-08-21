def test_logic(trace_id, span_id, flags):
    w3c_trace_id = "00-{:032x}-{:016x}-{}".format(
        trace_id,
        span_id,
        flags)
    return w3c_trace_id

# Test the logic
trace_id = 122259715594802403149644090040656830158
span_id = 98309129436836169
flags = 1

result = test_logic(trace_id, span_id, flags)
print(result)
