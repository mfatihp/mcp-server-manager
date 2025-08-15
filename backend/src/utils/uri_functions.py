from urllib.parse import urlparse




def url2uri_converter(url: str) -> str:
    pass
    



def uri2url_converter(uri: str, host: str, port: str) -> str:
    """Convert a URI to a full URL.

    Args:
        uri: URI string of the tool or resource.
        host: Server address.
        port: Server port number.
    
    Returns:
        str: URL of the MCP server.
    """

    parsed_url = urlparse(uri)
    converted_url = f"http://{host}:{port}{parsed_url.path}"
    return converted_url



if __name__ == "__main__":
    uri2url_converter(uri="tool://web/flightsim/buyticket", host="localhost", port="8000")