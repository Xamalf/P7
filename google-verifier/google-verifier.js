const express = require('express')
const app = express()
const port = 6000
const { OAuth2Client } = require('google-auth-library')
const client = new OAuth2Client(
  {
    clientId: process.env.CLIENTID,
    clientSecret: process.env.CLIENTSECRET,
    redirectUri: 'http://localhost:8080'
  }
)

app.use(express.json())
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
  console.log("VerifyCode entered, code: " + code)
  let { tokens } = await client.getToken(code)
  console.log("Printing tokens: " + tokens)
  client.setCredentials({ access_token: tokens.access_token })
  const userinfo = await client.request({
    url: 'https://www.googleapis.com/oauth2/v3/userinfo'
  })

  console.log(userinfo.data)

  return userinfo.data.email
}
