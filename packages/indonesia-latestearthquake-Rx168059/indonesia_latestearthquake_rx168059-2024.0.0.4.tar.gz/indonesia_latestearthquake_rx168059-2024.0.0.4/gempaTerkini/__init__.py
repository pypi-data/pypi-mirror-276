import requests
from bs4 import BeautifulSoup


def data_extract():
    """
    dateTime: date: 31 Mei 2024, time: 05:54:38 WIB
    magnitude: 5.4
    kedalaman: 88 km
    location: LS: 1.48, BT: 134.01
    pusat: 139 km BaratLaut PULAUKARATUNG-SULUT
    keterangan: tidak berpotensi TSUNAMI
    :return:
    """

    # catch error
    try:
        # get url
        content = requests.get("https://www.bmkg.go.id/")
    except Exception as e:
        print(e)
        return None

    if content.status_code == 200:

        # create BeautifulSoup object
        soup = BeautifulSoup(content.text, 'html.parser')

        # find span tag
        result_span = soup.find('span', {'class': 'waktu'})
        date = result_span.text.split(', ')[0]
        time = result_span.text.split(', ')[1]

        # find list tag in div tag
        result_div = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        li = result_div.findChildren('li')

        result_list = []

        # substain result_list value
        for i in range(len(li)):
            result_list.append(li[i].text)

        # remove not used value
        result_list.pop()

        # var
        magnitude = ''
        kedalaman = ''
        location = ''
        pusat = ''
        keterangan = ''

        # substain value to var
        i = 1
        while i < len(result_list):
            magnitude = result_list[i]
            i += 1
            kedalaman = result_list[i]
            i += 1
            location = result_list[i]
            i += 1
            pusat = result_list[i]
            i += 1
            keterangan = result_list[i]
            i += 1

        data_result = {
            'dateTime': {'date': date, 'time': time},
            'magnitude': magnitude,
            'kedalaman': kedalaman,
            'location': location,
            'pusat': pusat,
            'keterangan': keterangan,
        }
        return data_result
    else:
        return None


def show_data(datas):
    # error output
    if datas is None:
        print('data tidak ditemukan')
        return
    else:
        print(f'Date = {datas['dateTime']['date']}')
        print(f'Time = {datas['dateTime']['time']}')
        print(f'Magnitude = {datas['magnitude']}')
        print(f'kedalaman = {datas['kedalaman']}')
        print(f'location = {datas['location']}')
        print(f'pusat = {datas['pusat']}')
        print(f'keterangan = {datas['keterangan']}')


if __name__ == '__main__':
    print('Aplikasi utama')
    result = data_extract()
    show_data(result)
