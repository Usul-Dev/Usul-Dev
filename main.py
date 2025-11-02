import book_review

markdown_text = ''
markdown_text += """

## 📚 Latest Book Review

"""  # list of book review will be appended here

MAX_BOOK_REVIEW = 5
for idx, value in enumerate(book_review.main()):
    if idx >= MAX_BOOK_REVIEW:
        break
    else:
        markdown_text += f"- [{value['title']}]({value['url']})\n"

f = open('README.md', mode='w', encoding='utf-8')
f.write(markdown_text)
f.close()
