def modal():
    return html.Div(
        html.Div(
            [
                html.Div(
                    [   

                        # modal header
                        html.Div(
                            [
                                html.Span(
                                    "New Lead",
                                    style={
                                        "color": "#506784",
                                        "fontWeight": "bold",
                                        "fontSize": "20",
                                    },
                                ),
                                html.Span(
                                    "×",
                                    id="leads_modal_close",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),

                        # modal form
                        html.Div(
                            [
                                html.P(
                                    [
                                        "Company Name",
                                        
                                    ],
                                    style={
                                        "float": "left",
                                        "marginTop": "4",
                                        "marginBottom": "2",
                                    },
                                    className="row",
                                ),
                                dcc.Input(
                                    id="new_lead_company",
                                    # placeholder="Enter company name",
                                    type="text",
                                    value="",
                                    style={"width": "100%"},
                                ),
                                html.P(
                                    "Company State",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="new_lead_state",
                                    options=[
                                        {"label": state, "value": state}
                                        for state in states
                                    ],
                                    value="NY",
                                ),
                                html.P(
                                    "Status",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="new_lead_status",
                                    options=[
                                        {
                                            "label": "Open - Not Contacted",
                                            "value": "Open - Not Contacted",
                                        },
                                        {
                                            "label": "Working - Contacted",
                                            "value": "Working - Contacted",
                                        },
                                        {
                                            "label": "Closed - Converted",
                                            "value": "Closed - Converted",
                                        },
                                        {
                                            "label": "Closed - Not Converted",
                                            "value": "Closed - Not Converted",
                                        },
                                    ],
                                    value="Open - Not Contacted",
                                ),
                                html.P(
                                    "Source",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="new_lead_source",
                                    options=[
                                        {"label": "Web", "value": "Web"},
                                        {
                                            "label": "Phone Inquiry",
                                            "value": "Phone Inquiry",
                                        },
                                        {
                                            "label": "Partner Referral",
                                            "value": "Partner Referral",
                                        },
                                        {
                                            "label": "Purchased List",
                                            "value": "Purchased List",
                                        },
                                        {"label": "Other", "value": "Other"},
                                    ],
                                    value="Web",
                                ),
                            ],
                            className="row",
                            style={"padding": "2% 8%"},
                        ),

                        # submit button
                        html.Span(
                            "Submit",
                            id="submit_new_lead",
                            n_clicks=0,
                            className="button button--primary add"
                        ),
                    ],
                    className="modal-content",
                    style={"textAlign": "center"},
                )
            ],
            className="modal",
        ),
        id="leads_modal",
        style={"display": "none"},
)