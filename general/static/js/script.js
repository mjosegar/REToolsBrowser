
const buttons = document.querySelectorAll('.btn-table')
const tables = document.querySelectorAll('.category-table')
const selects = document.querySelectorAll('.category-select')

const submit_button = document.getElementById("submit-button")

const addedCategories = new Set();

const categoriesJson = document.getElementById("categories").getAttribute("data-categories")
const categories = JSON.parse(categoriesJson);

var remainingCategories;
function updateCategoryOptions() {
  remainingCategories = categories.filter(category => !addedCategories.has(category.id.toString()))

  if (remainingCategories.length == 0) {
    submit_button.disabled = false
    selects.forEach(select => {
      select.classList.add('d-none')
    })
    buttons.forEach(button => {
      button.classList.add('d-none')
    })
  } else {
    submit_button.disabled = true 
    selects.forEach(select => {
      select.classList.remove('d-none')
    })
    buttons.forEach(button => {
      button.classList.remove('d-none')
    })
  }
  selects.forEach(select => {
    select.innerHTML = ''
    remainingCategories.forEach(category => {
      const option = document.createElement('option')
      option.value = parseInt(category.id)
      option.textContent = category.topic
      select.appendChild(option)
    });
  });

}
buttons.forEach((button, i) => {
  button.addEventListener('click', () => {

    if (remainingCategories.length > 0) {
      const table = tables[i]
      const select = selects[i]

      const selectedCategoryId = select.value
      const selectedCategoryName = select.selectedOptions[0].textContent

      if (table.rows.length <= 4) {
        const tr = document.createElement('tr')
        const td1 = document.createElement('td')
        td1.textContent = selectedCategoryName
        const td2 = document.createElement('td')
        td2.style.textAlign = "right"

        const removeBtn = document.createElement('button')
        removeBtn.textContent = 'Delete'
        removeBtn.addEventListener('click', () => {
          tr.remove()
          addedCategories.delete(selectedCategoryId)
          updateCategoryOptions()
        });
        td2.appendChild(removeBtn)

        const td3 = document.createElement('td')
        td3.classList.add('p-0')
        const checkbox = document.createElement('input')
        checkbox.type = 'checkbox'
        checkbox.name = table.id
        checkbox.value = selectedCategoryId
        checkbox.checked = true
        checkbox.classList.add('d-none')
        checkbox.classList.add('checked')
        td3.appendChild(checkbox)

        tr.appendChild(td1)
        tr.appendChild(td2)
        tr.appendChild(td3)
        table.tBodies[0].appendChild(tr)

        addedCategories.add(selectedCategoryId.toString())
        updateCategoryOptions()
      } else {
        const modal = new bootstrap.Modal(document.getElementById("addCategoryModal"))
        modal.show()
      }
    }
  })
})

updateCategoryOptions()

const elementos = document.querySelectorAll('.sortable')
elementos.forEach(function (table) {
  Sortable.create(table, {
    animation: 150
  });
});




