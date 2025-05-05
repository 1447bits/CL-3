import xmlrpc.client

# Create an XML-RPC client
with xmlrpc.client.ServerProxy("http://localhost:8000/api/v1/rpc_handler") as proxy:
    try:
        # Replace 5 with the desired integer value
        input_value = int(input("Enter number: "))
        result = proxy.calculate_factorial(input_value)
        print(f"Factorial of {input_value} is: {result}")

        print(f"{input_value}'s square is {proxy.calculate_square(input_value)}")
    except Exception as e:
        print(f"Error: {e}")