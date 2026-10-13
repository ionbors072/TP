from tenacity import retry
from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)

print("\nPartea 1: Funcții")
print("build_url('https://example.com', '/login'):", build_url("https://example.com", "/login"))
print("build_url('https://example.com', 'login'):", build_url("https://example.com", "login"))
print("is_https('https://example.com'):", is_https("https://example.com"))
print("is_https('http://example.com'):", is_https("http://example.com"))

print("\nPartea 2:Trimiterea unei cereri")
print("show_response('https://example.com'):")
show_response("https://example.com")

print("show_response('http://this-site-does-not-exist.invalid'):")
show_response("http://this-site-does-not-exist.invalid")

print("\nPartea 3: Un verificator reutilizabil")
print("check_site('https://example.com'):", check_site("https://example.com"))
print("check_site('http://this-site-does-not-exist.invalid'):", check_site("http://this-site-does-not-exist.invalid"))

print("\nPartea 4: Verificarea mai multor site-uri")
scan_sites()