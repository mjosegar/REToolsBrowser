const buttons = document.querySelectorAll('.btn-modal')
const modal_button = document.getElementById('btn-modal-delete')

var id_button_clicked

buttons.forEach(button => {
  button.addEventListener('click', () => {
    id_button_clicked = button.id.split('-')[1]
  })
})

modal_button.addEventListener('click', () => window.location.href = window.location.origin+ '/tools/' + id_button_clicked + '/delete')