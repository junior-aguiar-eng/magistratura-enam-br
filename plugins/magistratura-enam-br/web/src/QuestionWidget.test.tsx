import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QuestionWidget } from "./QuestionWidget";
import type { Question } from "./contracts";

const ready: Question = { session_id: "qsn_1234567890abcdef", projection: "public", state: "ready", subject: "Processo Civil", topic: "Provas", prompt: "Assinale a alternativa correta.", alternatives: (["A","B","C","D","E"] as const).map((id) => ({ id, text: `Alternativa ${id}` })), source_status: "caution", caution_notice: "Fontes canônicas parcialmente disponíveis." };
const corrected: Question = { ...ready, projection: "corrected", state: "answered", selected_option: "B", correct_option: "C", result: "incorrect", correction: { correct_rationale: "A alternativa C observa o CPC.", distractor_analysis: [{option:"A",analysis:"Erro A"},{option:"B",analysis:"Erro B"},{option:"D",analysis:"Erro D"},{option:"E",analysis:"Erro E"}], exceptions: [], traps: [] } };

test("mostra cautela e mantém gabarito ausente antes da tentativa", () => {
  render(<QuestionWidget initialQuestion={ready} />);
  expect(screen.getByRole("alert")).toHaveTextContent("Cuidado");
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
  expect(screen.getAllByRole("radio")).toHaveLength(5);
  expect(screen.getByRole("button", {name:"Responder"})).toBeDisabled();
});

test("seleciona por teclado, envia e focaliza correção", async () => {
  const callTool = vi.fn().mockResolvedValue({ structuredContent: corrected });
  window.openai = { callTool };
  render(<QuestionWidget initialQuestion={ready} />);
  const radio = screen.getByRole("radio", {name:/Alternativa B/});
  radio.focus(); await userEvent.keyboard(" ");
  await userEvent.click(screen.getByRole("button", {name:"Responder"}));
  expect(callTool).toHaveBeenCalledWith("responder_questao", {session_id:ready.session_id, alternativa:"B"});
  expect((await screen.findByText(/gabarito C/)).closest("section")).toHaveFocus();
});

test("apresenta erro sem inventar correção", async () => {
  window.openai = { callTool: vi.fn().mockRejectedValue(new Error("offline")) };
  render(<QuestionWidget initialQuestion={ready} />);
  await userEvent.click(screen.getByRole("radio", {name:/Alternativa A/}));
  await userEvent.click(screen.getByRole("button", {name:"Responder"}));
  expect(await screen.findByText(/Não foi possível/)).toBeInTheDocument();
  expect(screen.queryByText(/gabarito/i)).not.toBeInTheDocument();
});

test("carrega a questão pelo formato de resultado do bridge MCP Apps", async () => {
  window.openai = undefined;
  render(<QuestionWidget />);
  expect(screen.getByText("Carregando questão…")).toBeInTheDocument();

  await act(async () => {
    window.dispatchEvent(new MessageEvent("message", {
      data: {
        jsonrpc: "2.0",
        method: "ui/notifications/tool-result",
        params: { structuredContent: ready },
      },
    }));
  });

  expect(await screen.findByRole("button", { name: "Responder" })).toBeInTheDocument();
  expect(screen.getByText(ready.prompt)).toBeInTheDocument();
});
