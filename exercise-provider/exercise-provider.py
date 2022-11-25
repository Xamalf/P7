from fastapi import FastAPI, HTTPException, Response
import requests
import uvicorn
from pydantic import BaseModel

app = FastAPI(root_path="/exercise-provider")

class Exercise_id(BaseModel):
    id: int

@app.post("/exercise-provider")
async def root(exercise_id: Exercise_id):
    try:
        auth_response = requests.post("http://auth.default:3000/auth", json={"name": "tester"}) # Calling auth
        # exercise_response = await data_base # Calling exercise database
        if auth_response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Auth failed"
            )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )

    with open("exercises/2.xml", "rb") as f:
        text = f.read()

    return Response(content=text, media_type="application/xml")

    jsonObject = {}

    jsonObject.update(
        {
            "preamble": """<?xml version="1.0" encoding="utf-8"?><!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'><nta><declaration>// Place global declarations here.clock t;</declaration>""",
        }
    )

    jsonObject.update(
        {
            "localDecl": """<declaration>// Place local declarations here.</declaration>"""
        }
    )

    jsonObject.update(
        {
            "template" : """<template><name x="5" y="5">Template</name><declaration>// Place local declarations here.</declaration><location id="id0" x="0" y="0"><name x="-10" y="-34">A</name><label kind="invariant" x="-17" y="17">t &lt; 4</label></location><location id="id1" x="127" y="0"><name x="117" y="-34">B</name><label kind="invariant" x="117" y="17">t &gt; 5</label><committed/></location><location id="id2" x="59" y="-93"><name x="49" y="-127">C</name><label kind="invariant" x="49" y="-76">t = 6</label><urgent/></location><init ref="id0"/><transition><source ref="id0"/><target ref="id1"/><label kind="select" x="18" y="-51">a</label><label kind="guard" x="18" y="-34">b</label><label kind="synchronisation" x="18" y="-17">c</label><label kind="assignment" x="18" y="0">d</label></transition></template>"""
        }
    )

    jsonObject.update(
        {
            "ending": """<system>// Place template instantiations here.Process = Template();// List one or more processes to be composed into a system.system Process;</system><queries><query><formula>E&lt;&gt; Process.B</formula><comment></comment></query><query><formula>Process.A --&gt; Process.B</formula><comment></comment></query></queries></nta>"""
        }
    )

    return jsonObject

uvicorn.run(app, host="0.0.0.0", port=2000)
