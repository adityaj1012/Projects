from hash_table import*
from dynamic_hash_table import*

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
def merge(left_array, right_array, left_start, left_end, right_start, right_end):
    merged_result = []
    left_index, right_index = left_start, right_start
    while left_index <= left_end and right_index <= right_end:
        if left_array[left_index] <= right_array[right_index]:
            merged_result.append(left_array[left_index])
            left_index += 1
        else:
            merged_result.append(right_array[right_index])
            right_index += 1
    merged_result.extend(left_array[left_index:left_end + 1])
    merged_result.extend(right_array[right_index:right_end + 1])
    return merged_result


def merge_sort(array, left, right):
    if left >= right:
        return
    middle = (left + right) // 2
    merge_sort(array, left, middle)
    merge_sort(array, middle + 1, right)
    merged_result = merge(array, array, left, middle, middle + 1, right)
    for i in range(left, right + 1):
        array[i] = merged_result[i - left]

def get_unique_elements(array):
    if len(array) <= 1:
        return array
    unique_elements = [array[0]]
    index = 1
    while index < len(array):
        if array[index] != unique_elements[-1]:
            unique_elements.append(array[index])
        index += 1
    return unique_elements

class MuskLibrary(DigitalLibrary):
    
    def __init__(self, book_titles, texts):
        self.book_titles = book_titles[:]
        self.texts = [text[:] for text in texts]
        self.manage = [(self.book_titles[i], self.texts[i]) for i in range(len(self.book_titles))]
        merge_sort(self.manage, 0, len(self.manage) - 1)
        for i in range(len(self.manage)):
            merge_sort(self.manage[i][1], 0, len(self.manage[i][1]) - 1)
            unique_text = get_unique_elements(self.manage[i][1])
            self.manage[i] = (self.manage[i][0], unique_text)

    
    def distinct_words(self, book_title):
        left, right = 0, len(self.manage) - 1

        while left <= right:
            middle = (left + right) // 2
            current_title = self.manage[middle][0]

            if current_title == book_title:
                return self.manage[middle][1]
            elif current_title < book_title:
                left = middle + 1
            else:
                right = middle - 1

    def count_distinct_words(self, book_title):
        left, right = 0, len(self.manage) - 1

        while left <= right:
            middle = (left + right) // 2
            current_title = self.manage[middle][0]

            if current_title == book_title:
                return len(self.manage[middle][1])
            elif current_title < book_title:
                left = middle + 1
            else:
                right = middle - 1

    def search_keyword(self, keyword):
        books_with_keyword = []
        for book_title, words in self.manage:
            left, right = 0, len(words) - 1
            while left <= right:
                middle = (left + right) // 2
                current_word = words[middle]
                if current_word == keyword:
                    books_with_keyword.append(book_title)
                    break
                elif current_word < keyword:
                    left = middle + 1
                else:
                    right = middle - 1
        return books_with_keyword

    def print_books(self):
        for book_title, words in self.manage:
            word_list = " | ".join(words)
            print(f"{book_title}: {word_list}")


class JGBLibrary(DigitalLibrary):
    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.books = []
        if name == "Jobs":
            self.collision = "Chain"
        elif name == "Gates":
            self.collision = "Linear"
        elif name == "Bezos":
            self.collision = "Double"
        else:
            raise ValueError("Invalid name provided. Expected 'Jobs', 'Gates', or 'Bezos'.")
        self.hashmap = HashMap(self.collision, params)

    
    def add_book(self, book_title, text):
        unique_words_set = HashSet(self.collision, self.params)
        for word in text:
            unique_words_set.insert(word)
        self.books.append((book_title, unique_words_set))
        self.hashmap.insert((book_title, unique_words_set))

    def distinct_words(self, book_title):
        distinct_words = []
        book_data = self.hashmap.find(book_title)
        if self.collision == "Chain":
            for bucket in book_data.hash_table:
                if bucket:
                    distinct_words.extend(bucket)
        elif self.collision in {"Linear", "Double"}:
            distinct_words.extend(word for word in book_data.hash_table if word)
        return distinct_words
    
    def count_distinct_words(self, book_title):
        book_data = self.hashmap.find(book_title)
        return book_data.item_count

    
    def search_keyword(self, keyword):
        ans=[]
        for book in self.books:
            if book[1].find(keyword):
                ans.append(book[0])
        return ans
    
    def print_books(self):
        for book_title, book_content in self.books:
            content_str = str(book_content)
            print(f"{book_title}: {content_str}")
