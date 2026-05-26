import React, {useState} from 'react';
export default function Login(){
  const [email,setEmail]=useState('');
  const [password,setPassword]=useState('');
  const [msg,setMsg]=useState('');
  const submit=async e=>{
    e.preventDefault();
    const res=await fetch('http://localhost:5000/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})});
    const j=await res.json();
    setMsg(j.message||'');
  };
  return (
    <form onSubmit={submit} style={{maxWidth:400}}>
      <h2>Login</h2>
      <div>
        <label>Email</label>
        <input value={email} onChange={e=>setEmail(e.target.value)} required />
      </div>
      <div>
        <label>Password</label>
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} required />
      </div>
      <button type="submit">Login</button>
      <div>{msg}</div>
    </form>
  );
}
