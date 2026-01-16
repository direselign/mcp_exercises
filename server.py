#lib
import logging
import sys
import argparse
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="Calculator")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers
    args:
        a: first number
        b: second number
    returns:
        sum of a and b
    """
    result = a + b
    logger.info(f"add({a}, {b}) = {result}")
    return result


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers
    args:
        a: first number
        b: second number
    returns:
        difference of a and b
    """
    result = a - b
    logger.info(f"subtract({a}, {b}) = {result}")
    return result


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers
    args:
        a: first number
        b: second number
    returns:
        product of a and b
    """
    result = a * b
    logger.info(f"multiply({a}, {b}) = {result}")
    return result


@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers
    args:
        a: first number
        b: second number
    returns:
        quotient of a and b
    """
    if b == 0:
        logger.error("Division by zero attempted")
        raise ValueError("Cannot divide by zero")
    result = a / b
    logger.info(f"divide({a}, {b}) = {result}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run local tool tests and exit")
    parser.add_argument("--stdio", action="store_true", help="Run FastMCP with stdio transport (default)")
    args = parser.parse_args()

    if args.test:
        logger.info("Running local tool tests...")
        print("add(2,3) ->", add(2,3))
        print("subtract(10,4) ->", subtract(10,4))
        print("multiply(6,7) ->", multiply(6,7))
        try:
            print("divide(8,2) ->", divide(8,2))
        except Exception as e:
            print("divide test error:", e)
        logger.info("Local tests completed.")
        sys.exit(0)

    logger.info("Starting Calculator MCP Server...")
    logger.info("Server is running and waiting for connections via stdio")
    try:
        mcp.run()  # stdio transport by default
    except KeyboardInterrupt:
        logger.info("Server interrupted by user.")
    except Exception:
        logger.exception("Server error encountered.")
        raise