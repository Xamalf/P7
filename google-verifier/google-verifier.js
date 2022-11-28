const express = require('express')
const app = express()
const port = 6000
const { OAuth2Client } = require('google-auth-library')
const client = new OAuth2Client(
  {
    clientId: process.env.clientId,
    clientSecret: process.env.clientSecret,
    redirectUri: 'http://localhost:8080'
  }
)

app.post('/google-verifier', (req, res) => {
  
  verifyCode(req.body.code).then((userInfo) => {
    res.send(userInfo)
  }).catch((error) => {
    console.log(error)
  })  
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})


// Call this function to validate OAuth2 authorization code sent from client-side
async function verifyCode(code) {
  let { tokens } = await client.getToken(code)
  client.setCredentials({ access_token: tokens.access_token })
  const userinfo = await client.request({
    url: 'https://www.googleapis.com/oauth2/v3/userinfo'
  })

  console.log(userinfo.data)

  return userinfo.data
}
