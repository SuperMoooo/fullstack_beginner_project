import React from 'react';
import TitleMicInput from './title_mic_input';

export default function ValidarParticipanteModal({
    setShowValidarParticipante,
    error,
    handleCaptureAudio,
    handleValidarParticipante,
    valorNif,
    setValorNif,
    valorCodigo,
    setValorCodigo,
    micListening,
}: {
    setShowValidarParticipante: any;
    error?: string;
    handleCaptureAudio: (setValor: any, valorAOuvir: string) => void;
    handleValidarParticipante: () => void;
    valorNif: string;
    setValorNif: any;
    valorCodigo: string;
    setValorCodigo: any;
    micListening: string;
}) {
    return (
        <main className="fixed flex items-center justify-center h-screen w-screen bg-black/50">
            <section className="w-fit flex flex-col gap-6 items-center justify-center *:text-center bg-white rounded-2xl p-6">
                <div
                    className="self-end cursor-pointer text-4xl"
                    onClick={() =>
                        setShowValidarParticipante((prev: boolean) => !prev)
                    }
                >
                    X
                </div>
                <h1 className="text-2xl self-start">
                    Insira os dados para entrar na atividade:
                </h1>
                <TitleMicInput
                    titulo="Nif"
                    handleCaptureAudio={() =>
                        handleCaptureAudio(setValorNif, 'nif')
                    }
                    valor={valorNif}
                    setValor={setValorNif}
                    micActive={micListening == 'nif'}
                />
                <TitleMicInput
                    titulo="Código"
                    handleCaptureAudio={() =>
                        handleCaptureAudio(setValorCodigo, 'codigo')
                    }
                    valor={valorCodigo}
                    setValor={setValorCodigo}
                    micActive={micListening == 'codigo'}
                />
                <button
                    type="button"
                    onClick={handleValidarParticipante}
                    className="cursor-pointer transition duration-300 border bg-blue-500 hover:bg-blue-900 text-white font-bold py-2 px-4 rounded self-end"
                >
                    Validar
                </button>
                {error && <p className="text-red-500 self-end">{error}</p>}
            </section>
        </main>
    );
}
