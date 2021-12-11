from pprint import pprint
import csv
import re
import pandas as pd

if __name__ == "__main__":


  with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
  pprint(contacts_list)

  correct_contact_list = [contacts_list[0]]
  for i in contacts_list[1:]:
      fio_list = re.findall('\w+', str(i[:3]))
      phone = re.sub('[^0-9]', '', i[5])
      phone = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(\d{4})', r'+7(\2)-\3-\4-\5 доб.\6', phone)
      phone = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)-\3-\4-\5', phone)
      correct_contact_list.append([fio_list[0], fio_list[1], fio_list[2] if len(fio_list) == 3 else '', i[3], i[4], phone, i[6]])
      

  correct_contact_list = pd.DataFrame(correct_contact_list)
  correct_contact_list = correct_contact_list.rename(columns=correct_contact_list.iloc[0])
  correct_contact_list = correct_contact_list[1:]
  pprint(correct_contact_list)
  correct_contact_list = correct_contact_list.groupby(['lastname', 'firstname']).agg(
      {'surname': 'max', 'organization': 'max', 'position': 'max', 'phone': 'max', 'email': 'max'}).reset_index()
  print(correct_contact_list)
  correct_contact_list.to_csv('phonebook.csv', index=False)

