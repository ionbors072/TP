
import httptools


def main():

    # Partea 1
    print("Partea 1")

    print(httptools.search({"q": "python", "page": "2"}))
    print(httptools.search({"q": "hello world & co"}))
    print(httptools.search_url({"q": "python", "page": "2"}))

    # Partea 2
    print("\nPartea 2")

    print(httptools.fetch_with_agent("MyBot/1.0"))
    print(httptools.default_agent())

    # Partea 3
    print("\nPartea 3")

    print(httptools.post_json({
        "name": "Ana",
        "age": 19,
        "tags": ["a", "b"]
    }))

    print(httptools.post_form({
        "user": "ana",
        "city": "Bălți"
    }))

    # Partea 4
    print("\nPartea 4")

    print(httptools.describe_status(200))
    print(httptools.describe_status(404))
    print(httptools.describe_status(503))

    print(httptools.is_ok(204))
    print(httptools.is_ok(500))

    # Partea 5
    print("\nPartea 5")

    print(httptools.count_redirects(3))
    print(httptools.final_url(2))
    print(httptools.first_hop(3))

    # Partea 6
    print("\nPartea 6")

    print(httptools.cookie_demo("theme", "dark"))
    print(httptools.no_session_demo("theme", "dark"))

    # Partea 7
    print("\nPartea 7")

    rezultate = []

    for path in httptools.PATHS:
        rezultat = httptools.report(path)
        rezultat["path"] = path
        rezultate.append(rezultat)

    reusite = []

    for rezultat in rezultate:
        if rezultat["status"] == 200:
            reusite.append(rezultat)

    reusite.sort(
        key=lambda x: x["seconds"],
        reverse=True
    )

    for rezultat in reusite:
        print(
            rezultat["path"],
            "->",
            rezultat["status"],
            ",",
            round(rezultat["seconds"], 2),
            "secunde"
        )

    print(
        "Reusite:", len(reusite),
        "| Esuate:", len(rezultate) - len(reusite)
    )

    # Partea 8: Bonus
    print("\nPartea 8")

    print(httptools.check_login("admin", "secret"))
    print(httptools.check_login("admin", "gresit"))


if __name__ == "__main__":
    main()
