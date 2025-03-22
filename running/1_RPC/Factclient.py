import xmlrpc.client

# Create an XML-RPC client
with xmlrpc.client.ServerProxy("http://localhost:8000/server") as proxy:
    try:
        
        inp = 12
        result = proxy.calculate_factorial(inp)
        print(f"Factorial of {inp} is: {result}")

        inp = 2
        pow = 5
        result = proxy.pow(inp, pow)
        print(f"{pow}th power of {inp} is: {result}")

    except Exception as e:
        print(f"Error: {e}")
