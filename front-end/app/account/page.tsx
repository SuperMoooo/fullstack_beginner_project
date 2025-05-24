'use client';
import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import TitleInput from '../components/title_input';
import { Tipo } from '../util/types';
import Loading from '../components/loading';

export default function Account() {
    const [nome, setNome] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [data_nascimento, setDataNascimento] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [tipo, setTipo] = useState<Tipo>('admin');
    const [nif, setNif] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        getUserData();
    }, []);

    const getUserData = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const nome = localStorage.getItem('user_nome');
            const response = await fetch(
                `http://127.0.0.1:5000/get-user/${nome}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            if (response.ok) {
                const auxData = await response.json();
                const data = auxData['Data'];
                setNome(data['nome']);
                setEmail(data['email']);
                setDataNascimento(data['data_nascimento']);
                setTipo(data['tipo']);
                setPassword(data['password']);
                if (data['tipo'] == 'user') {
                    setNif(data['user']);
                }
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setError('Servidor Offline');
            } else {
                setError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };
    // ATUALIZAR
    const handleUpdateUserInfo = async () => {};
    return (
        <main className="grid grid-rows-[auto_1fr] min-h-[100dvh]">
            <Navbar goBack={true} isConta={true} />
            <section className="flex items-center justify-start w-full p-20 flex-col gap-10">
                <h1 className=" text-2xl">Conta</h1>
                {loading ? (
                    <Loading />
                ) : (
                    <form
                        onSubmit={handleUpdateUserInfo}
                        className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col w-2/4 p-10"
                    >
                        <div className="w-full flex items-start justify-between flex-col gap-2">
                            <h1 className="text-lg">Tipo de Utilizador</h1>
                            <select
                                name="tipo"
                                id="tipo"
                                onChange={(e) =>
                                    setTipo(e.target.value as Tipo)
                                }
                                className="rounded-md border border-gray-300 bg-gray-100 p-2 outline-none w-full"
                            >
                                <option value="admin">Admin</option>
                                <option value="user">Usuário</option>
                                <option value="participante">
                                    Participante
                                </option>
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
                            readOnly={true}
                            setValor={setDataNascimento}
                            valor={data_nascimento}
                            titulo="Data de nascimento"
                            error={error.toLocaleLowerCase().includes('data')}
                        />
                        <TitleInput
                            setValor={setPassword}
                            valor={password}
                            titulo="Password"
                            inputType="password"
                            error={error
                                .toLocaleLowerCase()
                                .includes('password')}
                        />

                        {tipo == 'user' && (
                            <TitleInput
                                setValor={setNif}
                                valor={nif}
                                titulo="Nif"
                                error={error
                                    .toLocaleLowerCase()
                                    .includes('nif')}
                            />
                        )}

                        <button
                            className="border rounded-2xl text-white bg-blue-500 p-4 w-full cursor-pointer hover:bg-blue-400"
                            type="submit"
                        >
                            Atualizar Dados
                        </button>
                        {error && !error.includes('undefined') && (
                            <p className="text-red-500">{error}</p>
                        )}
                    </form>
                )}
            </section>
        </main>
    );
}
