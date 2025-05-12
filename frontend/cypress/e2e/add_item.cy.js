describe('Add item to todo list', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let backend_port = 5001;

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
          console.log(uid);
        })
    })


  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')
  })

  it('create a task', () => {
    const data = {
      userid: uid,
      title: "Test task",
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
      })
  })

  it('login to the system with the account', () => {
    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
    // alternative, imperative way of detecting that input field
    //cy.get('.inputwrapper #email')
    //    .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // TODO assert task exists
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
      url: `http://localhost:${backend_port}/tasks/byid/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
