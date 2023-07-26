document.addEventListener('DOMContentLoaded', () => {
    let choice = document.querySelectorAll('.choice')
    choice.forEach((button) => {
        button.addEventListener('click', () => {
            switch (button.id) {
                case 'gold':
                    button.style.backgroundColor = 'red'
                    break
                case 'silver':
                    button.style.backgroundColor = 'red'
                    break
                case 'guess':
                    button.style.backgroundColor = '#4CAF50'
                    break
            }
        })

    })

})