from textnode import TextNode, TextType

def main():
    # sample nodes
    plain = TextNode("Hello world", TextType.PLAIN)
    bold = TextNode("Strong!", TextType.BOLD)
    link = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(plain)
    print(bold)
    print(link)

if __name__ == "__main__":
    main()
