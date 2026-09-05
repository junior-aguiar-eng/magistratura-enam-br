def test_caso_complexo_exige_fatos_funcionais_e_solucoes_concorrentes(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/casos-complexos.md").casefold()
    for requisito in (
        "fatos funcionalmente relevantes",
        "questões jurídicas",
        "soluções concorrentes",
        "pressuposto decisivo",
        "entendimento prevalente",
    ):
        assert requisito in referencia


def test_correcao_classifica_a_origem_do_erro(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/casos-complexos.md").casefold()
    for erro in ("identificação", "enquadramento", "fonte", "inferência", "conclusão"):
        assert erro in referencia
