// Test case R8UC1

describe('Add item to todo list', () => {
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

  it('toggle task from active to done', () => {
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

    cy.get('.todo-item')
      .should('be.visible')

    cy.get('.checker')
      .should('have.class', 'unchecked')

    cy.get('.todo-item').get('.editable')
      .should('have.css', 'text-decoration')
      .should('not.include', 'line-through')

    cy.get('.checker')
      .click()
    
    cy.get('.checker')
      .should('have.class', 'checked')

    cy.get('.todo-item').find('.editable')
      .should('have.css', 'text-decoration')
      .should('include', 'line-through')
  })

  it('toggle task from done to active', () => {
    //    data.append('data', `{'$set': {'done': ${!todo.done}}}`);

  const data = {
    data: JSON.stringify({
      $set: {
        done: true
      }
    })
  };

    
    cy.request({
      method: 'PUT',
      url: `http://localhost:${backend_port}/todos/byid/${todoid}`,
      form: true,
      body: data
      }).then((response) => {
        console.log(response)
      })
    cy.visit('http://localhost:3000')

    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    cy.get('form')
      .submit()

    // assert task exists
    cy.get('.title-overlay')
      .should('contain.text', 'Important task')

    cy.get('.done-check')
      .click()

    cy.get('.todo-item')
      .should('be.visible')

    cy.get('.checker')
      .should('have.class', 'checked')

    cy.get('.todo-item').find('.editable')
      .should('have.css', 'text-decoration')
      .should('include', 'line-through')

    cy.get('.checker')
      .click()
    
    cy.get('.checker')
      .should('have.class', 'unchecked')

    cy.get('.todo-item').get('.editable')
      .should('have.css', 'text-decoration')
      .should('not.include', 'line-through')

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
