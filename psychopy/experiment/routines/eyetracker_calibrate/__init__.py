from .. import BaseStandaloneRoutine
from psychopy.localization import _translate
from psychopy.experiment import Param
from pathlib import Path
from psychopy.alerts import alert


class EyetrackerCalibrationRoutine(BaseStandaloneRoutine):
    categories = ['Eyetracking']
    targets = ["PsychoPy"]
    iconFile = Path(__file__).parent / "eyetracker_calib.png"
    tooltip = _translate("Calibration routine for eyetrackers")
    beta = True

    def __init__(self, exp, name='calibration',
                 progressMode="time", targetDur=1.5, expandDur=1, expandScale=1.5,
                 movementAnimation=True, movementDur=1.0, targetDelay=1.0,
                 innerFillColor='green', innerBorderColor='black', innerBorderWidth=2, innerRadius=0.0035,
                 fillColor='', borderColor="black", borderWidth=2, outerRadius=0.01,
                 colorSpace="rgb", units='from exp settings',
                 targetLayout="NINE_POINTS", randomisePos=True,
                 disabled=False
                 ):
        # Initialise base routine
        BaseStandaloneRoutine.__init__(self, exp, name=name, disabled=disabled)

        self.exp.requirePsychopyLibs(['iohub', 'hardware'])

        # Basic params
        self.order += [
            "targetLayout",
            "randomisePos",
        ]

        del self.params['stopVal']
        del self.params['stopType']

        self.params['targetLayout'] = Param(targetLayout,
                                            valType='str', inputType="choice", categ='Basic',
                                            allowedVals=['THREE_POINTS', 'FIVE_POINTS', 'NINE_POINTS', "THIRTEEN_POINTS"],
                                            hint=_translate("Pre-defined target layouts"),
                                            label=_translate("Target Layout"))

        self.params['randomisePos'] = Param(randomisePos,
                                            valType='bool', inputType="bool", categ='Basic',
                                            hint=_translate("Should the order of target positions be randomised?"),
                                            label=_translate("Randomise Target Positions"))

        # Target Params
        self.order += [
            "targetStyle",
            "fillColor",
            "borderColor",
            "innerFillColor",
            "innerBorderColor",
            "colorSpace",
            "borderWidth",
            "innerBorderWidth",
            "outerRadius",
            "innerRadius",
        ]

        self.params['innerFillColor'] = Param(innerFillColor,
                                     valType='color', inputType="color", categ='Target',
                                     hint=_translate("Fill color of the inner part of the target"),
                                     label=_translate("Inner Fill Color"))

        self.params['innerBorderColor'] = Param(innerBorderColor,
                                           valType='color', inputType="color", categ='Target',
                                           hint=_translate("Border color of the inner part of the target"),
                                           label=_translate("Inner Border Color"))

        self.params['fillColor'] = Param(fillColor,
                                         valType='color', inputType="color", categ='Target',
                                         hint=_translate("Fill color of the outer part of the target"),
                                         label=_translate("Outer Fill Color"))

        self.params['borderColor'] = Param(borderColor,
                                           valType='color', inputType="color", categ='Target',
                                           hint=_translate("Border color of the outer part of the target"),
                                           label=_translate("Outer Border Color"))

        self.params['colorSpace'] = Param(colorSpace,
                                          valType='str', inputType="choice", categ='Target',
                                          allowedVals=['rgb', 'dkl', 'lms', 'hsv'],
                                          hint=_translate(
                                              "In what format (color space) have you specified the colors? (rgb, dkl, lms, hsv)"),
                                          label=_translate("Color Space"))

        self.params['borderWidth'] = Param(borderWidth,
                                           valType='num', inputType="single", categ='Target',
                                           hint=_translate("Width of the line around the outer part of the target"),
                                           label=_translate("Outer Border Width"))

        self.params['innerBorderWidth'] = Param(innerBorderWidth,
                                           valType='num', inputType="single", categ='Target',
                                           hint=_translate("Width of the line around the inner part of the target"),
                                           label=_translate("Inner Border Width"))

        self.params['outerRadius'] = Param(outerRadius,
                                           valType='num', inputType="single", categ='Target',
                                           hint=_translate("Size (radius) of the outer part of the target"),
                                           label=_translate("Outer Radius"))

        self.params['innerRadius'] = Param(innerRadius,
                                           valType='num', inputType="single", categ='Target',
                                           hint=_translate("Size (radius) of the inner part of the target"),
                                           label=_translate("Inner Radius"))

        self.params['units'] = Param(units,
                                     valType='str', inputType="choice", categ='Target',
                                     allowedVals=['from exp settings'],
                                     hint=_translate("Units of dimensions for this stimulus"),
                                     label=_translate("Spatial Units"))

        # Animation Params
        self.order += [
            "progressMode",
            "targetDur",
            "expandDur",
            "expandScale",
            "movementAnimation",
            "movementDur",
            "targetDelay"
        ]

        self.params['progressMode'] = Param(progressMode,
                                            valType="str", inputType="choice", categ="Animation",
                                            allowedVals=["space key", "time"],
                                            hint=_translate("Should the target move to the next position after a "
                                                            "keypress or after an amount of time?"),
                                            label=_translate("Progress Mode"))

        self.depends.append(
            {"dependsOn": "progressMode",  # must be param name
             "condition": "in ['time', 'either']",  # val to check for
             "param": "targetDur",  # param property to alter
             "true": "show",  # what to do with param if condition is True
             "false": "hide",  # permitted: hide, show, enable, disable
             }
        )

        self.params['targetDur'] = Param(targetDur,
                                         valType='num', inputType="single", categ='Animation',
                                         hint=_translate(
                                             "Time limit (s) after which progress to next position"),
                                         label=_translate("Target Duration"))

        self.depends.append(
            {"dependsOn": "progressMode",  # must be param name
             "condition": "in ['space key', 'either']",  # val to check for
             "param": "expandDur",  # param property to alter
             "true": "show",  # what to do with param if condition is True
             "false": "hide",  # permitted: hide, show, enable, disable
             }
        )

        self.params['expandDur'] = Param(expandDur,
                                         valType='num', inputType="single", categ='Animation',
                                         hint=_translate(
                                             "Duration of the target expand/contract animation"),
                                         label=_translate("Expand / Contract Duration"))

        self.params['expandScale'] = Param(expandScale,
                                           valType='num', inputType="single", categ='Animation',
                                           hint=_translate("How many times bigger than its size the target grows"),
                                           label=_translate("Expand Scale"))

        self.params['movementAnimation'] = Param(movementAnimation,
                                                 valType='bool', inputType="bool", categ='Animation',
                                                 hint=_translate(
                                                     "Enable / disable animations as target stim changes position"),
                                                 label=_translate("Animate Position Changes"))

        self.depends.append(
            {"dependsOn": "movementAnimation",  # must be param name
             "condition": "== True",  # val to check for
             "param": "movementDur",  # param property to alter
             "true": "show",  # what to do with param if condition is True
             "false": "hide",  # permitted: hide, show, enable, disable
             }
        )

        self.params['movementDur'] = Param(movementDur,
                                           valType='num', inputType="single", categ='Animation',
                                           hint=_translate(
                                               "Duration of the animation during position changes."),
                                           label=_translate("Movement Duration"))

        self.depends.append(
            {"dependsOn": "movementAnimation",  # must be param name
             "condition": "== False",  # val to check for
             "param": "targetDelay",  # param property to alter
             "true": "show",  # what to do with param if condition is True
             "false": "hide",  # permitted: hide, show, enable, disable
             }
        )

        self.params['targetDelay'] = Param(targetDelay,
                                           valType='num', inputType="single", categ='Animation',
                                           hint=_translate(
                                               "Duration of the delay between positions."),
                                           label=_translate("Target Delay"))

    def writeMainCode(self, buff):
        # Alert user if eyetracking isn't setup
        if self.exp.eyetracking == "None":
            alert(code=4505)
        # Get inits
        inits = self.params
        # Code-ify 'from exp settings'
        if self.params['units'].val == 'from exp settings':
            inits['units'].val = None
        # Synonymise expand dur and target dur
        if inits['progressMode'].val == 'time':
            inits['expandDur'] = inits['targetDur']
        if inits['progressMode'].val == 'space key':
            inits['targetDur'] = inits['expandDur']
        # Synonymise movement dur and target delay
        if inits['movementAnimation'].val:
            inits['targetDelay'] = inits['movementDur']
        else:
            inits['movementDur'] = inits['targetDelay']

        BaseStandaloneRoutine.writeMainCode(self, buff)

        # Make target
        code = (
            "# define target for %(name)s\n"
            "%(name)sTarget = visual.TargetStim(win, \n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
                "name='%(name)sTarget',\n"
                "radius=%(outerRadius)s, fillColor=%(fillColor)s, borderColor=%(borderColor)s, lineWidth=%(borderWidth)s,\n"
                "innerRadius=%(innerRadius)s, innerFillColor=%(innerFillColor)s, innerBorderColor=%(innerBorderColor)s, innerLineWidth=%(innerBorderWidth)s,\n"
                "colorSpace=%(colorSpace)s, units=%(units)s\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")"
        )
        buff.writeIndentedLines(code % inits)
        # Make config object
        code = (
            "# define parameters for %(name)s\n"
            "%(name)s = hardware.eyetracker.EyetrackerCalibration(win, \n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
                "eyetracker, %(name)sTarget,\n"
                "units=%(units)s, colorSpace=%(colorSpace)s,\n"
                "progressMode=%(progressMode)s, targetDur=%(targetDur)s, expandScale=%(expandScale)s,\n"
                "targetLayout=%(targetLayout)s, randomisePos=%(randomisePos)s,\n"
                "movementAnimation=%(movementAnimation)s, targetDelay=%(targetDelay)s\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")\n"
            "# run calibration\n"
            "%(name)s.run()\n"
            "# clear any keypresses from during %(name)s so they don't interfere with the experiment\n"
            "defaultKeyboard.clearEvents()\n"
        )
        buff.writeIndentedLines(code % inits)
