import React from 'react';
import TitleInput from './title_input';
import TitleSelect from './title_select';

export default function AtividadeForm({
    title,
    handleSubmit,
    setAddAtividade,
    setDescricaoAtividade,
    descricaoAtividade,
    errorAtividade,
    setDataAtividade,
    dataAtividade,
    setHoraAtividade,
    horaAtividade,
    setLocalAtividade,
    localAtividade,
    restricoesPossiveis,
    setRestricoes,
    restricaoInicial,
    nomeBotao,
}: {
    title: string;
    handleSubmit: any;
    setAddAtividade: any;
    setDescricaoAtividade: any;
    descricaoAtividade: string;
    errorAtividade: string;
    setDataAtividade: any;
    dataAtividade: string;
    setHoraAtividade: any;
    horaAtividade: string;
    setLocalAtividade: any;
    localAtividade: string;
    restricoesPossiveis: string[];
    setRestricoes: any;
    restricaoInicial?: any;
    nomeBotao: string;
}) {
    return (
        <section className="top-0 left-0 fixed w-screen h-screen flex items-center justify-center">
            <div className="bg-black opacity-60 top-0 left-0 fixed h-screen w-screen -z-10"></div>

            <form
                onSubmit={handleSubmit}
                className="flex items-end justify-center gap-6 flex-col w-1/3 p-10 bg-white rounded-2xl"
            >
                <button
                    className="text-5xl cursor-pointer"
                    type="button"
                    onClick={() => setAddAtividade((prev: boolean) => !prev)}
                >
                    X
                </button>
                <div className="flex items-center justify-start w-full">
                    <h1 className="text-4xl">{title}</h1>
                </div>
                <TitleInput
                    titulo="Descrição da Atividade"
                    setValor={setDescricaoAtividade}
                    valor={descricaoAtividade}
                    error={errorAtividade.includes('descrição')}
                />
                <TitleInput
                    titulo="Data da Atividade"
                    setValor={setDataAtividade}
                    valor={dataAtividade}
                    inputType="date"
                    error={errorAtividade.includes('data')}
                />
                <TitleInput
                    titulo="Hora da Atividade"
                    setValor={setHoraAtividade}
                    valor={horaAtividade}
                    inputType="time"
                    error={errorAtividade.includes('hora')}
                />
                <TitleInput
                    titulo="Local da Atividade"
                    setValor={setLocalAtividade}
                    valor={localAtividade}
                    error={errorAtividade.includes('local')}
                />
                <TitleSelect
                    initialValor={restricaoInicial}
                    title="Restrições"
                    valores={restricoesPossiveis}
                    setValor={setRestricoes}
                />
                <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                >
                    {nomeBotao}
                </button>
                {errorAtividade && !errorAtividade.includes('undefined') && (
                    <p className="text-red-500">{errorAtividade}</p>
                )}
            </form>
        </section>
    );
}
