writefile = open('write.csv', 'a+', encoding='cp1251')
writefile.write('Тест' + ',' + 'Первый')
writefile.close()

writefile = open('write.csv', 'r', encoding='cp1251')
for line in writefile:
    print(line)