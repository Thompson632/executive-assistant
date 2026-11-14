// JavaScript for Automation. Read metadata from already running macOS clients.

function singleMatch(collection, name) {
    const matches = collection.whose({name: name})().filter(item => item.name() === name);
    if (matches.length !== 1) {
        throw new Error("EA_SELECTION");
    }
    return matches[0];
}

function mail(app, options, start, end) {
    const account = singleMatch(app.accounts, options.mailAccount);
    const folder = singleMatch(account.mailboxes, options.mailFolder);
    const messages = folder.messages.whose({_and: [
        {dateReceived: {_greaterThanEquals: start}},
        {dateReceived: {_lessThan: end}},
        {deletedStatus: false},
        {_or: [{readStatus: false}, {flaggedStatus: true}]}
    ]})();
    return messages
        .map(message => ({message, received: message.dateReceived()}))
        .sort((a, b) => b.received - a.received)
        .slice(0, options.limit)
        .map(({message, received}) => ({
            subject: String(message.subject() || "(No subject)"),
            sender: String(message.sender() || ""),
            received: received.toISOString(),
            folder: options.mailFolder,
            unread: !message.readStatus(),
            flagged: message.flaggedStatus()
        }));
}

function calendar(app, options, start, end) {
    const selected = singleMatch(app.calendars, options.calendarName);
    const events = selected.events.whose({
        startDate: {_lessThan: end},
        endDate: {_greaterThan: start}
    })();
    return events.map(event => ({
        // The Calendar scripting dictionary does not expose event privacy.
        title: options.includeCalendarTitles ? String(event.summary() || "Calendar event") : "Calendar event",
        start: event.startDate().toISOString(),
        end: event.endDate().toISOString(),
        all_day: event.alldayEvent(),
        status: String(event.status())
    }));
}

function run(argv) {
    const [kind, rawOptions] = argv;
    const options = JSON.parse(rawOptions);
    const start = new Date(options.start);
    const end = new Date(options.end);
    const appName = kind === "mail" ? "Mail" : "Calendar";
    const app = Application("/System/Applications/" + appName + ".app");
    if (!app.running()) {
        throw new Error("EA_NOT_RUNNING");
    }
    return JSON.stringify(kind === "mail" ? mail(app, options, start, end) : calendar(app, options, start, end));
}
