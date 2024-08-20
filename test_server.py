from turtle import update
import requests


def test_server():

    url = "http://localhost:5000"
    endpoint = "/a2l/update"

    a2l_path = "test/arm_project/test.a2l"
    elf_path = "test/arm_project/out/test_structs.elf"

    response = requests.post(
        url + endpoint, files={"a2l": open(a2l_path, "rb"), "elf": open(elf_path, "rb")}
    )
    data = response.json()
    updated_a2l = data["a2l"]

    with open(a2l_path, "w") as f:
        f.write(updated_a2l)


if __name__ == "__main__":
    test_server()
