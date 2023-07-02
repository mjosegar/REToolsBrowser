const checkboxes = document.querySelectorAll('.form-check-search')
const submit_button = document.getElementById('submit-button')

const rows = document.querySelectorAll('.row-search')

var categories_selected = 0

rows.forEach(row => {
    row.addEventListener('click', () => {
        var row_id = row.id
        row_id = row_id.split("-")[1];

        row.querySelector('input[type="checkbox"]');
        var checkbox = document.querySelector('.form-check-search#checkbox-'+ row_id)

        var row_class_selected
        if (row_id%2 == 0)
            row_class_selected = 'row-selected-pair'
        else 
            row_class_selected = 'row-selected-odd'

        if (row.classList.contains(row_class_selected)){
            row.classList.remove(row_class_selected)
            checkbox.checked = false
            categories_selected -= 1
        } else {
            row.classList.add(row_class_selected)
            checkbox.checked = true
            categories_selected += 1
        }

        go_next_step()
    })
})

function go_next_step() {
    if (categories_selected > 0)
        submit_button.disabled = false
    else
        submit_button.disabled = true
}
