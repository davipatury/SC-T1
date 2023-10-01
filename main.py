alphabet = [c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

def repeat_key(key, lgt):
  repeats = lgt // len(key) + 1
  return (key * repeats)[:lgt]

def encrypt(text, key):
  text = text.upper()
  key = repeat_key(key, len(text))
  out = ""
  i = 0
  for c in text:
    if c in alphabet:
      out += alphabet[(ord(c) + ord(key[i])) % 26]
      i += 1
    else:
      out += c
  return out

def decrypt(text, key):
  text = text.upper()
  key = repeat_key(key, len(text))
  out = ""
  i = 0
  for c in text:
    if c in alphabet:
      out += alphabet[(ord(c) - ord(key[i]) % 26 + 26) % 26]
      i += 1
    else:
      out += c
  return out

def valid_chars(text):
  return ''.join([c for c in text if c.upper() in alphabet])

def key_size(text):
  text = valid_chars(text)
  interval = []
  for i in range(len(text) - 2):
    trigram = text[i] + text[i+1] + text[i+2]
    for j in range(i+1, len(text)-2):
      cand = text[j] + text[j+1] + text[j+2]
      if cand == trigram:
        interval.append(j - i)
    
  freq = {}
  for intv in set(interval):
    for i in range(2, 21):
      if intv % i == 0:
        freq[i] = freq.get(i, 0) + 1
  
  key_s = (0, 0)
  freq = dict(sorted(freq.items(), key = lambda i: i[1], reverse = True))

  print("----- Possiveis tamanhos de chaves -----")
  print("--------- Tamanho | Quantidade ---------")
  for key, value in freq.items():
    if value >= key_s[1]:
      key_s = (key, value)
    print(f"{str(key).rjust(17, ' ')} | {value}")

  print(f"--------- Tamanho provável = {key_s[0]} ---------")
  inp = input("Gostaria de trocar o tamanho da chave? (S/N)\n> ")
  if inp.upper() == "S":
    return int(input("Digite o tamanho de chave desejado:\n> "))

  return key_s[0]

letter_freq = {
  'en': [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074],
  'pt': [14.63, 1.04, 3.88, 4.99, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]
}
def find_letter(prob, lang):
  lang = lang.lower()
  letter = ''
  total_diff = 999999999 # very high initial value

  for i in range(26):
    diff = sum(abs(prob[(i+j) % 26] - letter_freq[lang][j]) for j in range(26))
    if diff < total_diff:
      letter = alphabet[i]
      total_diff = diff

  return letter

def break_encryption(key, text, lang):
  text = valid_chars(text)
  keyword = ""
  for i in range(key):
    total = 0
    freq = {}
    prob = []
    for j in range(i, len(text), key):
      freq[text[j]] = freq.get(text[j], 0) + 1
      total += 1
    
    for c in alphabet:
      prob.append(freq.get(c, 0) / total * 100)
    
    keyword += find_letter(prob, lang)
  return keyword

def options():
  print('------ Cifra de Vigenère ------')
  print('1 - Cifrar')
  print('2 - Decifrar')
  print('3 - Ataque')
  print('4 - Sair')
  print('-------------------------------')
  return input("> ")

def main():
  while True:
    option = options()
    if option == '1':
      text = input("Digite o texto que você gostaria de cifrar: ")
      key = input("Digite a chave: ")
      encrypted_text = encrypt(text, key)
      print(f"Texto cifrado: {encrypted_text}")
    elif option == '2':
      text = input("Digite o texto que você gostaria de decifrar: ")
      key = input("Digite a chave: ")
      decrypted_text = decrypt(text, key)
      print(f"Texto decifrado: {decrypted_text}")
    elif option == '3':
      text = input("Digite o texto que você gostaria de atacar: ")
      lang = input("Digite a linguagem do texto (PT/EN): ")

      key_s = key_size(text)
      keyword = break_encryption(key_s, text.upper(), lang)

      print("Palavra-chave: ", keyword)
      print(f"Mensagem decifrada: {decrypt(text, keyword)}")
    else:
      break

main()
