// Test case R8UC3

describe('Remove item to todo list', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let email // email of the user
  let taskid // task id
  let todoid // todo id
  let backend_port = Cypress.env('backend_port');

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: `http://localhost:${backend_port}/users/create`,
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
    })
  })

  beforeEach(function () {
    // enter the main main page
    const data = {
      userid: uid,
      title: "Important task",
      description: "description",
      url: "Sl6en1NPTYM",
      todos: "Watch video"
    }

    cy.request({
        method: 'POST',
        url: `http://localhost:${backend_port}/tasks/create`,
        form: true,
        body: data
      }).then((response) => {
        console.log(response)
        taskid = response.body[0]._id.$oid
        todoid = response.body[0].todos[0]._id.$oid
      })
  })

  afterEach(() => {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:${backend_port}/tasks/byid/${taskid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })

  it('delete item from todo list', () => {
    cy.visit('http://localhost:3000')

    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    cy.get('form')
      .submit()

    // assert task exists
    cy.get('.title-overlay')
      .should('contain.text', 'Important task')

    cy.get('img')
      .click()

    cy.contains('span.editable', 'Watch video')
      .closest('.todo-item')
      .find('.remover')
      .click()

    cy.contains('span.editable', 'Watch video')
      .closest('.todo-item')
      .should('not.exist')
  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:${backend_port}/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
    // clean up by deleting the task from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:${backend_port}/tasks/byid/${taskid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
