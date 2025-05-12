describe('Add item to todo list', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
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

  it('starting out on the landing screen', () => {
    // make sure the landing page contains a header with "login"
    cy.get('h1')
      .should('contain.text', 'Login')
  })

  it('login to the system with an existing account', () => {

    const data = new URLSearchParams();
      data.append('title', 'Test task');
      data.append('description', '(add a description here)');
      data.append('userid', uid);
        
    cy.request({
        method: 'POST',
        url: 'http://localhost:5000/tasks/create',
        body: "apa"
      }).then((response) => {
        console.log(response)
      })
  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
    // clean up by deleting the task from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/tasks/byid/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
