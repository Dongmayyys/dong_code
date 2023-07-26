document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('submit').addEventListener('click', () => {
        let selectElement = document.getElementById('lifetime')
        let selectedOption = selectElement.options[selectElement.selectedIndex].value
        let response = document.getElementById('response')
        let date = new Date()
        switch(selectedOption){
            case '20':
                response.innerHTML = `${2003+20}年，有些人还活着，但他已经死了`
                break
            case '99':
                response.innerHTML = `${2003+99}年，切记要珍惜时间啊，骚年`
                break
            case '128':
                response.innerHTML = `${2003+128}年，恭喜你活了2^7个年头，差一步美满`
                break
            case '256':
                response.innerHTML = `${2003+256}年，恭喜你活了2^8个年头，整整1个字节的大小`
                break
        }
    })

})