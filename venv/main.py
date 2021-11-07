import companion_finder
def main():
    cur, conn = companion_finder.open_database()
    companion_finder.find_companions(cur)
    companion_finder.close_database(conn)


if __name__ == '__main__':
    main()