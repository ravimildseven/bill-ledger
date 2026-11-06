"""Builds the 'Log Spend' iPhone Shortcut for Bill Ledger as an unsigned plist."""
import plistlib, sys, uuid

OWNER, REPO, FILE = "ravimildseven", "bill-ledger-data", "bill-ledger.json"
API = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/"
OBJ = "￼"

def U(): return str(uuid.uuid4()).upper()
def out(u, name): return {"Type": "ActionOutput", "OutputUUID": u, "OutputName": name}
def att(a): return {"Value": a, "WFSerializationType": "WFTextTokenAttachment"}
def tts(*parts):
    """Text with inline variables: parts are str or attachment dicts."""
    s, rng = "", {}
    for p in parts:
        if isinstance(p, str): s += p
        else:
            rng["{%d, 1}" % (len(s.encode("utf-16-le")) // 2)] = p   # UTF-16 offset
            s += OBJ
    v = {"string": s}
    if rng: v["attachmentsByRange"] = rng
    return {"Value": v, "WFSerializationType": "WFTextTokenString"}
def dictfield(items):
    return {"Value": {"WFDictionaryFieldValueItems": [
        {"WFItemType": t, "WFKey": tts(k), "WFValue": v} for k, t, v in items]},
        "WFSerializationType": "WFDictionaryFieldValue"}
def act(ident, **p): return {"WFWorkflowActionIdentifier": "is.workflow.actions." + ident, "WFWorkflowActionParameters": p}

TOKEN = {"Type": "Variable", "VariableName": "Token"}
def headers():
    return dictfield([
        ("Authorization", 0, tts("Bearer ", TOKEN)),
        ("Accept", 0, tts("application/vnd.github.raw+json")),
        ("X-GitHub-Api-Version", 0, tts("2022-11-28")),
    ])

t, ledger, parsed, quick, cards, card, amt, cats, cat, note, when, entry, text, b64, put, ok, msg, why = (
    U() for _ in range(18))
grp, guard = U(), U()
A = [
    act("gettext", UUID=t, WFTextActionText="PASTE_YOUR_GITHUB_TOKEN"),
    act("setvariable", WFVariableName="Token", WFInput=att(out(t, "Text"))),
    act("downloadurl", UUID=ledger, WFURL=API + FILE, WFHTTPMethod="GET",
        ShowHeaders=True, WFHTTPHeaders=headers()),
    # GitHub labels the raw file application/vnd.github.raw+json, which Shortcuts
    # does not treat as JSON on its own — parse it explicitly.
    act("detect.dictionary", UUID=parsed, WFInput=att(out(ledger, "Contents of URL"))),
    act("getvalueforkey", UUID=quick, WFGetDictionaryValueType="Value", WFDictionaryKey="quick",
        WFInput=att(out(parsed, "Dictionary"))),
    # No card list means GitHub refused the request (usually the token) or the
    # app hasn't published the list yet. Say which, and stop.
    act("conditional", GroupingIdentifier=guard, WFControlFlowMode=0, WFCondition=101,
        WFInput={"Type": "Variable", "Variable": att(out(quick, "Dictionary Value"))}),
    act("getvalueforkey", UUID=why, WFGetDictionaryValueType="Value", WFDictionaryKey="message",
        WFInput=att(out(parsed, "Dictionary"))),
    act("alert", WFAlertActionTitle="Couldn't load your cards",
        WFAlertActionMessage=tts("GitHub said: ", out(why, "Dictionary Value"),
            "\n\nIf that says Bad credentials or Not Found, the token is wrong or lacks Contents access "
            "to bill-ledger-data — edit the shortcut and paste it again. If it's blank, open the "
            "ledger app once so it publishes your card list."),
        WFAlertActionCancelButtonShown=False),
    act("exit"),
    act("conditional", GroupingIdentifier=guard, WFControlFlowMode=2),
    act("getvalueforkey", UUID=cards, WFGetDictionaryValueType="Value", WFDictionaryKey="cards",
        WFInput=att(out(quick, "Dictionary Value"))),
    act("choosefromlist", UUID=card, WFInput=att(out(cards, "Dictionary Value")),
        WFChooseFromListActionPrompt="Which card?"),
    act("ask", UUID=amt, WFInputType="Number", WFAskActionPrompt="How much?",
        WFAskActionAllowsDecimalNumbers=True, WFAskActionAllowsNegativeNumbers=False),
    act("getvalueforkey", UUID=cats, WFGetDictionaryValueType="Value", WFDictionaryKey="cats",
        WFInput=att(out(quick, "Dictionary Value"))),
    act("choosefromlist", UUID=cat, WFInput=att(out(cats, "Dictionary Value")),
        WFChooseFromListActionPrompt="What for?"),
    act("ask", UUID=note, WFInputType="Text", WFAskActionPrompt="Where? (optional)",
        WFAskActionDefaultAnswer=""),
    act("format.date", UUID=when, WFDateFormatStyle="Custom", WFDateFormat="yyyy-MM-dd'T'HH-mm-ss",
        WFDate=tts({"Type": "CurrentDate"})),
    act("dictionary", UUID=entry, WFItems=dictfield([
        ("card", 0, tts(out(card, "Chosen Item"))),
        ("amount", 3, tts(out(amt, "Provided Input"))),
        ("cat", 0, tts(out(cat, "Chosen Item"))),
        ("note", 0, tts(out(note, "Provided Input"))),
        ("at", 0, tts(out(when, "Formatted Date"))),
    ])),
    act("detect.text", UUID=text, WFInput=att(out(entry, "Dictionary"))),
    act("base64encode", UUID=b64, WFEncodeMode="Encode", WFBase64LineBreakMode="None",
        WFInput=att(out(text, "Text"))),
    act("downloadurl", UUID=put,
        WFURL=tts(API + "inbox/", out(when, "Formatted Date"), ".json"),
        WFHTTPMethod="PUT", ShowHeaders=True, WFHTTPHeaders=headers(),
        WFHTTPBodyType="JSON", WFJSONValues=dictfield([
            ("message", 0, tts("Quick add from iPhone")),
            ("content", 0, tts(out(b64, "Base64 Encoded"))),
        ])),
    act("getvalueforkey", UUID=ok, WFGetDictionaryValueType="Value", WFDictionaryKey="content",
        WFInput=att(out(put, "Contents of URL"))),
    act("conditional", GroupingIdentifier=grp, WFControlFlowMode=0, WFCondition=100,
        WFInput={"Type": "Variable", "Variable": att(out(ok, "Dictionary Value"))}),
    act("notification", WFNotificationActionTitle="Logged",
        WFNotificationActionBody=tts(out(amt, "Provided Input"), " on ", out(card, "Chosen Item"),
                                     " · ", out(cat, "Chosen Item")),
        WFNotificationActionSound=False),
    act("conditional", GroupingIdentifier=grp, WFControlFlowMode=1),
    act("getvalueforkey", UUID=msg, WFGetDictionaryValueType="Value", WFDictionaryKey="message",
        WFInput=att(out(put, "Contents of URL"))),
    act("notification", WFNotificationActionTitle="Couldn't log it",
        WFNotificationActionBody=tts("GitHub said: ", out(msg, "Dictionary Value"))),
    act("conditional", GroupingIdentifier=grp, WFControlFlowMode=2),
]

wf = {
    "WFWorkflowClientVersion": "2605.0.5",
    "WFWorkflowMinimumClientVersion": 900,
    "WFWorkflowMinimumClientVersionString": "900",
    "WFWorkflowIcon": {"WFWorkflowIconStartColor": 463140863, "WFWorkflowIconGlyphNumber": 59511},
    "WFWorkflowTypes": [],
    "WFWorkflowInputContentItemClasses": [],
    "WFWorkflowOutputContentItemClasses": [],
    "WFWorkflowHasOutputFallback": False,
    "WFWorkflowHasShortcutInputVariables": False,
    "WFWorkflowImportQuestions": [{
        "ActionIndex": 0, "Category": "Parameter", "ParameterKey": "WFTextActionText",
        "DefaultValue": "",
        "Text": "Paste a GitHub token that can read and write Contents on bill-ledger-data (the same kind of token the app's sync uses).",
    }],
    "WFWorkflowActions": A,
}
plistlib.dump(wf, open(sys.argv[1], "wb"), fmt=plistlib.FMT_BINARY)
print("actions:", len(A))
