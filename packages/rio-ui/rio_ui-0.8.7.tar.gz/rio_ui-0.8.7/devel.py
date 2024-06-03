import rio
from datetime import date
from dataclasses import KW_ONLY
import calendar


class RootComponent(rio.Component):
    value: date = date.today()

    def build(self) -> rio.Component:
        return rio.Column(
            rio.Calendar(
                value=self.bind().value,
                align_x=0.5,
                align_y=0.5,
            ),
            rio.DateInput(
                label="Pick a date",
                value=self.bind().value,
                align_x=0.5,
                align_y=0.5,
            ),
        )


app = rio.App(
    build=RootComponent,
)


# app.run_in_browser(
#     port=8001,
# )
