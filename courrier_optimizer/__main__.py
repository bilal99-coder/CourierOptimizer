from Models.BaseEntity import BaseEntity
from datetime import datetime

def main():
    print("hello world")
    c = BaseEntity("hello", datetime.now(), datetime.now())
    print(c.id)
    print(c.created)

if __name__ == '__main__':
    main()
