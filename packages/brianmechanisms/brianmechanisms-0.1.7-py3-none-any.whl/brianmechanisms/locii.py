import numpy as np
import re
import copy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Locii:
    def __init__(self, links, configs):
        self.links = links
        self.configs = configs

    def getPivot(self, link):
        for key, value in link.get("points").items():
            if value == 0:
                return key

    def getOrigin(self, link):
        origin = link.get("origin")
        if origin is not None and origin[0] == "{" and origin[-1] == "}":
            return tuple(map(float, origin[1:-1].split(',')))
        else:
            link_name, point = origin.split(".")
            return self.links.get(link_name).get("positions").get(point)

    def extract_variables(self, equation):
        pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        matches = pattern.findall(equation)
        functions = {"np", "sin", "cos", "tan", "log", "exp", "sqrt"}
        variables = [match for match in matches if match not in functions]
        return variables

    def replace_variables(self, equation, replacements):
        def replacer(match):
            var = match.group(0)
            return replacements.get(var, var)
        pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        new_equation = pattern.sub(replacer, equation)
        return new_equation

    def evaluateKeys(self, link, keys_to_evaluate):
        for key in keys_to_evaluate:
            if key in link:
                value = link[key]
                if isinstance(value, str):
                    if value[0:4] == "link":
                        link_name, link_key = value.split(".")
                        link[key] = self.links.get(link_name).get(f"calculated_{link_key}")
                    else:
                        equation_variables = self.extract_variables(value)
                        replacements = {}
                        for variable in equation_variables:
                            if variable[0:4] == "link":
                                link_name, link_key = variable.split(".")
                                replacements[variable] = str(self.links.get(link_name).get(f"calculated_{link_key}"))
                            else:
                                replace = link.get(f"calculated_{variable}") if f"calculated_{variable}" in link else link.get(variable) if variable in link else None
                                if replace is not None:
                                    replacements[variable] = f"{replace}"
                        link[key] = self.replace_variables(value, replacements)
                else:
                    link[f"calculated_{key}"] = value
        return link

    def getLowestStepDifference(self):
        links = self.links
        second_points = []
        for link in links:            
            if list(links[link]["positions"].values())[0] != (0, 0):
                second_point = list(links[link]["positions"].values())[1]
                second_points.append(second_point)
        y_values = [point[1] for point in second_points]
        sorted_y_values = sorted(y_values)
        lowest_y = sorted_y_values[0]
        second_lowest_y = sorted_y_values[1]
        difference = second_lowest_y - lowest_y
        return lowest_y, second_lowest_y, difference
    
    def plotStepHeight(self):
        fig, axs = plt.subplots(1, 2)
        step_heights = []
        lowest_ys = []
        theta_range = np.arange(0, 361, 1)
        for theta in theta_range:
            paths = self.outputPath(np.arange(theta, theta + 1, 1))
            lowest_y, _, difference = self.getLowestStepDifference()
            lowest_ys.append(lowest_y)
        lowest_y = min(lowest_ys)

        actual_steps = []
        for theta in theta_range:
            paths = self.outputPath(np.arange(theta, theta + 1, 1))
            paths = paths[0]
            lowest_y_for_step, _, difference = self.getLowestStepDifference()
            actual_step = lowest_y_for_step - lowest_y
            actual_steps.append(actual_step)
            step_heights.append(difference)


        axs[0].set_title('Diff btn 2 lowest legs')
        axs[0].plot(np.arange(0, 361, 1), step_heights)
        axs[0].set_xlabel('Theta')
        axs[0].set_ylabel('Step Height')
        # mark on the plot the x and y value of the step_heights
        min_step_height = min(step_heights)
        max_step_height = max(step_heights)
        min_theta = theta_range[step_heights.index(min_step_height)]
        max_theta = theta_range[step_heights.index(max_step_height)]

        lowest_y_at_lowest_step = lowest_ys[step_heights.index(min_step_height)]
        step_height_at_lowest_y = lowest_y_at_lowest_step - lowest_y

        axs[0].annotate(f'Min: {min_step_height:.2f}, {min_theta:.2f}', xy=(min_theta, min_step_height), 
                    xytext=(min_theta, min_step_height + 0.05),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    horizontalalignment='center')
        
        axs[0].annotate(f'Max: {max_step_height:.2f}', xy=(max_theta, max_step_height), 
                    xytext=(max_theta, max_step_height - 0.1),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    horizontalalignment='center')
        
        # plot also actual steps
        axs[1].set_title('Step Height')
        axs[1].plot(np.arange(0, 361, 1), actual_steps)
        axs[1].set_xlabel('Theta')
        axs[1].set_ylabel('Actual Step Height')
        
        min_actual_step = min(actual_steps)
        max_actual_step = max(actual_steps)
        min_theta = theta_range[actual_steps.index(min_actual_step)]
        max_theta = theta_range[actual_steps.index(max_actual_step)]

        axs[1].annotate(f'Min: {min_actual_step:.2f}, {min_theta:.2f}', xy=(min_theta, min_actual_step),
                    xytext=(min_theta, min_actual_step + 0.002),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    horizontalalignment='center')
        
        axs[1].annotate(f'Max: {max_actual_step:.5f}', xy=(max_theta, max_actual_step),
                    xytext=(max_theta, max_actual_step - 0.002),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    horizontalalignment='center')
        
        return fig, axs

    def rotate_point(self, point, theta0):
        x, y = point
        theta = np.radians(theta0)  # Convert angle from degrees to radians
        x_prime = x * np.cos(theta) - y * np.sin(theta)
        y_prime = x * np.sin(theta) + y * np.cos(theta)
        return x_prime, y_prime

    def calculatePositions(self, link, theta, linkConfigs={}):
        for key, value in linkConfigs.items():
            link[key] = value
            if isinstance(value, str):
                if value[0:4] == "link":
                    link_name, link_key = value.split(".")
                    link[key] = self.links.get(link_name).get(link_key)
                else:
                    link[key] = eval(value)
            else:
                link[key] = value

        keys_to_evaluate = ["speed", "speed_factor", "speed_source", "equation"]
        link = self.evaluateKeys(link, keys_to_evaluate)

        link["calculated_origin"] = self.getOrigin(link)
        theta0 = link.get("theta0") if "theta0" in link else 0
        theta = np.deg2rad(theta)
        theta0 = np.deg2rad(theta0)
        thetaRotation = self.configs.get("thetaRotation") if "thetaRotation" in self.configs else 0
        positions = {}
        for key in link.get("points").keys():
            positions[key] = (None, None)
        pivot = self.getPivot(link)
        equation = link.get("equation")
        points = link.get("points")
        len_factor = link.get("len_factor") if "len_factor" in link else 1
        if isinstance(len_factor, str):
            len_factor = eval(len_factor)

        for pointName, length in points.items():
            length = float(length)
            if pointName == pivot:
                point = link.get("calculated_origin") 
            else:
                x_eq, y_eq = equation.split(',')
                unrotatedOrigin = link.get("calculated_origin") # do not rotate a point that has been rotated
                unrotatedOrigin = self.rotate_point(unrotatedOrigin, -thetaRotation) 
                x_position = len_factor * length * eval(x_eq.replace("x", str(theta0 + theta))) + unrotatedOrigin[0]
                y_position = len_factor * length * eval(y_eq.replace("x", str(theta0 + theta))) + unrotatedOrigin[1]
                point = (x_position, y_position)
                point = self.rotate_point(point, thetaRotation) # Rotate the point
            positions[pointName] =  point#(x_position, y_position) #
        link["positions"] = positions
        return link

    def outputPath(self, thetaRange=None):
        if thetaRange is None:
            thetaRange = np.arange(0, 361, 1)
        paths = []
        for theta in thetaRange:
            thetaPoints = {}
            for key, link in self.links.items():
                link = self.calculatePositions(link, theta, self.configs[key] if key in self.configs else {})
                thetaPoints[key] = link["positions"]
            paths.append(thetaPoints)
        return paths

    def plotOutPutPaths(self, title={"title": "Output Paths of Links", "sub": None}, plotConfig={"fig": None, "ax": None, "legend": True, "axes": True}):
        fig = plotConfig["fig"]
        ax = plotConfig["ax"]
        if fig is None:
            fig, ax = plt.subplots()
        paths = self.outputPath()
        for link_key, link in self.links.items():
            x_values = {key: [] for key in link["points"].keys()}
            y_values = {key: [] for key in link["points"].keys()}
            output_point = link.get("output")
            pivot = self.getPivot(link)
            for thetaPoints in paths:
                for point, (x, y) in thetaPoints.get(link_key).items():
                    if point != pivot:
                        x_values[point].append(x)
                        y_values[point].append(y)
            for point in x_values.keys():
                if point != pivot:
                    linestyle = 'solid' if point == output_point else 'dotted'
                    ax.plot(x_values[point], y_values[point], label=f'{point}', linestyle=linestyle)

        if ("axes" in plotConfig and plotConfig["axes"]) or "axes" not in plotConfig:
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
        else:
            ax.axis('off')
        fig.suptitle(title["title"], fontsize=16)

        if "sub" in title and title["sub"] is not None:
            ax.set_title(title["sub"])

        ax.set_aspect('equal', adjustable='box')
        if ("legend" in plotConfig and plotConfig["legend"]) or "legend" not in plotConfig:
            ax.legend()

        if "mechanism_theta" in plotConfig:
            mechanism_theta = plotConfig["mechanism_theta"]
            links_mechanism = copy.deepcopy(self.links)
            paths = self.outputPath(np.arange(mechanism_theta, mechanism_theta + 1, 1))
            paths = paths[0]

            all_points = {}
            for link_key, link in paths.items():
                for point, (x, y) in link.items():
                    all_points[point] = (x, y)
            x_coords = [coords[0] for coords in all_points.values()]
            y_coords = [coords[1] for coords in all_points.values()]
            ax.scatter(x_coords, y_coords, color='red')

            for link_key, link in self.links.items():
                points = list(link["points"].keys())
                for i in range(len(points) - 1):
                    x_values = [all_points[points[i]][0], all_points[points[i + 1]][0]]
                    y_values = [all_points[points[i]][1], all_points[points[i + 1]][1]]
                    ax.plot(x_values, y_values, linestyle='solid', label=f'{points[i]} to {points[i + 1]}')

        return fig, ax

    def update(self, mechanism_theta, ax, title, plotConfig):
        ax.clear()
        links_mechanism = copy.deepcopy(self.links)
        paths = self.outputPath()
        for link_key, link in self.links.items():
            x_values = {key: [] for key in link["points"].keys()}
            y_values = {key: [] for key in link["points"].keys()}
            output_point = link.get("output")
            pivot = self.getPivot(link)
            for thetaPoints in paths:
                for point, (x, y) in thetaPoints.get(link_key).items():
                    if point != pivot:
                        x_values[point].append(x)
                        y_values[point].append(y)
            for point in x_values.keys():
                if point != pivot:
                    linestyle = 'solid' if point == output_point else 'dotted'
                    ax.plot(x_values[point], y_values[point], label=f'{point}', linestyle=linestyle)

        paths = self.outputPath(np.arange(mechanism_theta, mechanism_theta + 1, 1))
        paths = paths[0]

        all_points = {}
        for link_key, link in paths.items():
            for point, (x, y) in link.items():
                all_points[point] = (x, y)

        x_coords = [coords[0] for coords in all_points.values()]
        y_coords = [coords[1] for coords in all_points.values()]
        ax.scatter(x_coords, y_coords, color='red')

        for link_key, link in self.links.items():
            points = list(link["points"].keys())
            for i in range(len(points) - 1):
                x_values = [all_points[points[i]][0], all_points[points[i + 1]][0]]
                y_values = [all_points[points[i]][1], all_points[points[i + 1]][1]]
                ax.plot(x_values, y_values, linestyle='solid', label=f'{points[i]} to {points[i + 1]}')

        if ("axes" in plotConfig and plotConfig["axes"]) or "axes" not in plotConfig:
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
        else:
            ax.axis('off')

        if "sub" in title and title["sub"] is not None:
            ax.set_title(title["sub"])

        ax.set_aspect('equal', adjustable='box')
        if ("legend" in plotConfig and plotConfig["legend"]) or "legend" not in plotConfig:
            ax.legend()

    def clearPath(self, pathName):
        self.paths.pop(pathName, None)

    def savePath(self, pathName, path):
        self.paths[pathName] = path
