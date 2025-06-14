// Test case R8UC1

describe('Add item to todo list', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let taskid // task id
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

  it('add new task', () => {
    cy.visit('http://localhost:3000')
    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // assert task exists
    cy.get('.title-overlay')
      .should('contain.text', 'Important task')

    cy.get('img')
      .click()

    cy.get('input[placeholder=\"Add a new todo item\"]')
      .type('New todo')

    // Assert add button active and click
    cy.contains('Add')
      .should('not.be.disabled')
      .click()

    // Assert new todo is added
    cy.contains('New todo').should('be.visible')
  })


  it('assert add button is disabled', () => {
    cy.visit('http://localhost:3000')
    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // assert task exists
    cy.get('.title-overlay')
      .should('contain.text', 'Important task')

    cy.get('img')
      .click()

    cy.get('input[placeholder=\"Add a new todo item\"]')
      .should('be.visible')
    // Assert add button disabled
    cy.contains('Add')
      .should('be.disabled')
  })

    it('assert add button is active', () => {
    cy.visit('http://localhost:3000')
    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // assert task exists
    cy.get('.title-overlay')
      .should('contain.text', 'Important task')

    cy.get('img')
      .click()

    cy.get('input[placeholder=\"Add a new todo item\"]')
      .type('New task')
    // Assert add button active
    cy.contains('Add')
      .should('not.be.disabled')
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
