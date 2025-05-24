'use client';
import Link from 'next/link';
import React, { useState } from 'react';
import Loading from '../components/loading';
import TitleInput from '../components/title_input';
import { Tipo } from '../util/types';

export default function RegisterPage() {
    const [nome, setNome] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [data_nascimento, setDataNascimento] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [tipo, setTipo] = useState<Tipo>('admin');
    const [nif, setNif] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    // HANDLE REGISTER
    const register = async (e: any) => {
        try {
            e.preventDefault();
            let day = data_nascimento.split('-')[2];
            let month = data_nascimento.split('-')[1].split('-')[0];
            let year = data_nascimento.split('-')[0];
            const birthDate = `${day}/${month}/${year}`;

            setLoading(true);
            if (nome == '' || password == '' || email == '') {
                alert('Preencha todos os campos!');
                setError('Preencha todos os campos!');
                return;
            }
            let response;
            if (tipo == 'user') {
                response = await fetch('http://127.0.0.1:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        nome: nome,
                        email: email,
                        data_nascimento: birthDate,
                        password: password,
                        tipo: tipo,
                        nif: nif,
                    }),
                });
            } else {
                response = await fetch('http://127.0.0.1:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        nome: nome,
                        email: email,
                        data_nascimento: birthDate,
                        password: password,
                        tipo: tipo,
                    }),
                });
            }

            // SALVAR TOKEN E LIMITE
            if (response.ok) {
                alert('Sucesso');
                window.location.href = '/login';
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] || 'Erro desconhecido');
                alert(errorData['Erro'] || 'Erro desconhecido');
            }
        } catch (error: any) {
            setError(error.message);
            alert('Erro ao fazer login');
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="grid grid-rows-[auto_1fr] h-[100dvh]">
            <header className="flex justify-start items-center p-6 border-b border-gray-300">
                <Link href={{ pathname: '/login' }} className="text-4xl">
                    &#60; Voltar
                </Link>
            </header>
            <section className="flex items-center justify-center ">
                <form
                    className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col p-10 w-1/3"
                    onSubmit={register}
                >
                    <h1 className="text-3xl">Criar conta</h1>
                    <div className="w-full flex items-start justify-between flex-col gap-2">
                        <h1 className="text-lg">Tipo de Utilizador</h1>
                        <select
                            name="tipo"
                            id="tipo"
                            onChange={(e) => setTipo(e.target.value as Tipo)}
                            className="rounded-md border border-gray-300 bg-gray-100 p-2 outline-none w-full"
                        >
                            <option value="admin">Admin</option>
                            <option value="user">Usuário</option>
                            <option value="participante">Participante</option>
                        </select>
                    </div>

                    <TitleInput
                        setValor={setNome}
                        valor={nome}
                        titulo="Nome"
                        error={error.toLocaleLowerCase().includes('nome')}
                    />
                    <TitleInput
                        setValor={setEmail}
                        valor={email}
                        titulo="Email"
                        inputType="text"
                        error={error.toLocaleLowerCase().includes('email')}
                    />
                    <TitleInput
                        setValor={setDataNascimento}
                        valor={data_nascimento}
                        titulo="Data de nascimento"
                        inputType="date"
                        error={error.toLocaleLowerCase().includes('data')}
                    />
                    <TitleInput
                        setValor={setPassword}
                        valor={password}
                        titulo="Password"
                        inputType="password"
                        error={error.toLocaleLowerCase().includes('password')}
                    />

                    {tipo == 'user' && (
                        <TitleInput
                            setValor={setNif}
                            valor={nif}
                            titulo="Nif"
                            error={error.toLocaleLowerCase().includes('nif')}
                        />
                    )}

                    <button
                        className="border rounded-2xl text-white bg-blue-500 p-4 w-full cursor-pointer hover:bg-blue-400"
                        type="submit"
                    >
                        Entrar
                    </button>
                    {error && !error.includes('undefined') && (
                        <p className="text-red-500">{error}</p>
                    )}
                    <h3>
                        Já tem conta?{' '}
                        <Link
                            href={{ pathname: '/login' }}
                            className="underline text-blue-700"
                        >
                            Entrar!
                        </Link>
                    </h3>
                </form>
                {loading && <Loading />}
            </section>
        </main>
    );
}
