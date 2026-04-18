import streamlit as st
import bitstring as bit

if 'loggedin' not in st.session_state:
    st.session_state.loggedin = False
if 'users' not in st.session_state:
    st.session_state.users = ["new","new"]
if 'files' not in st.session_state:
    st.session_state.files = []


for x in range(len(st.session_state.files)):
    if 'image' in st.session_state.files[x][2]:
        st.write(st.session_state.files[x][0]+":")
        st.image(st.session_state.files[x][1])
    else:
        st.download_button("Download "+st.session_state.files[x][0],data=st.session_state.files[x][1],file_name=st.session_state.files[x][0], key=x)

if not st.session_state.loggedin:
    username = st.text_input("Username")
    password = st.text_input("Password")
    if st.button("Log in"):
        if username in st.session_state.users and st.session_state.users[st.session_state.users.index(username)+1] == password:
            st.session_state.loggedin = True
        else:
            st.write("Not authenticated. Press 'Sign up' button.")
    if st.button("Sign up"):
        st.session_state.users.append(username)
        st.session_state.users.append(password)
    
if st.session_state.loggedin:
    if st.button("Log out"):
        st.session_state.loggedin = False
    st.session_state.M = st.file_uploader("Upload a file to be hidden.")
    if type(st.session_state.M) is __file__:
        st.write(len(bit.BitArray(st.session_state.M.getvalue())))
    st.session_state.P = st.file_uploader("Upload a carrier.")
    st.session_state.D = st.file_uploader("Upload a file to decrypt.")
    st.session_state.S = st.text_input("Starting bit.")
    st.session_state.L = st.text_input("Bit spacing.")
    st.session_state.size = st.text_input("Hidden message length in bits.")
    st.session_state.C = st.radio("Mode of Operation", ["No variation","Three-tier variation"])
    if st.button("Encrypt"):
        carrier = bit.BitArray(st.session_state.P.getvalue())
        message = bit.BitArray(st.session_state.M.getvalue())
        index = int(st.session_state.S)
        for x in range(len(message)):
            if st.session_state.C == "No variation":
                if carrier[index] != message[x]:
                    carrier.overwrite(bit.BitArray(message[x]),index)
                index += int(st.session_state.L)
            if st.session_state.C == "Three-tier variation":
                if(x%3 == 0):
                    if carrier[index] != message[x]:
                        carrier.overwrite(bit.BitArray(message[x]),index)
                    index += int(st.session_state.L)*2
                if(x%3 == 1):
                    if carrier[index] != message[x]:
                        carrier.overwrite(bit.BitArray(message[x]),index)
                    index += int(st.session_state.L)*4
                if(x%3 == 2):
                    if carrier[index] != message[x]:
                        carrier.overwrite(bit.BitArray(message[x]),index)
                    index += int(st.session_state.L)
        output = open('newfile', 'wb')
        bit.Bits(carrier).tofile(output)
        output.close()
        output= open('newfile', 'rb')
        fileOut = output.read()
        output.close()
        st.session_state.files.append([st.session_state.P.name,fileOut,st.session_state.P.type])
        st.rerun()
    if st.button("Decrypt"):
        carrier = bit.BitArray(st.session_state.D.getvalue())
        index = int(st.session_state.S)
        for x in range(int(st.session_state.size)):
            if st.session_state.C == "No variation":
                if x == 0:
                    out = bit.BitArray(carrier[index])
                else:
                    out.append(bit.BitArray(carrier[index]))
                index += int(st.session_state.L)
            if st.session_state.C == "Three-tier variation":
                if x == 0:
                    out = bit.BitArray(carrier[index])
                    index += int(st.session_state.L)*2
                if(x%3 == 0):
                    out.append(bit.BitArray(carrier[index]))
                    index += int(st.session_state.L)*2
                if(x%3 == 1):
                    out.append(bit.BitArray(carrier[index]))
                    index += int(st.session_state.L)*4
                if(x%3 == 2):
                    out.append(bit.BitArray(carrier[index]))
                    index += int(st.session_state.L)
        output = open('newfile', 'wb')
        bit.Bits(out).tofile(output)
        output.close()
        output= open('newfile', 'rb')
        fileOut = output.read()
        output.close()
        st.download_button("Download hidden message.", fileOut)