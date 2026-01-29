from PyQt5.QtGui import QColor, QFontMetrics, QIcon, QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QColorDialog,
    QFontComboBox,
    QGroupBox,
    QLabel,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QScrollArea,
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt
from krita import *
import math

class RSBGDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rogudator's Speech Bubble Generator V2")
        
        # --- UI SETUP ---
        mainLayout = QVBoxLayout()

        # Botón para añadir a la página
        self.addOnPage = QPushButton("Add on Page")
        mainLayout.addWidget(self.addOnPage)

        # Previsualización
        previewLabel = QLabel("Preview")
        mainLayout.addWidget(previewLabel)

        self.preview = QSvgWidget(self)
        self.preview.setMinimumHeight(250)
        mainLayout.addWidget(self.preview)

        # Selección de Tipo de Burbuja
        bubbleTypes = QGroupBox()
        bubbleTypes.setTitle("Bubble Type")
        bubbleTypesLayout = QHBoxLayout()
        
        self.typeSquare = QRadioButton("Square")
        self.typeSharpSquare = QRadioButton("Sharp Box")
        self.typeRound = QRadioButton("Round")
        self.typeCloud = QRadioButton("Cloud (Think)") # Nuevo
        self.typeShout = QRadioButton("Shout (Scream)") # Nuevo
        
        self.typeRound.setChecked(True)
        
        bubbleTypesLayout.addWidget(self.typeSquare)
        bubbleTypesLayout.addWidget(self.typeSharpSquare)
        bubbleTypesLayout.addWidget(self.typeRound)
        bubbleTypesLayout.addWidget(self.typeCloud)
        bubbleTypesLayout.addWidget(self.typeShout)
        
        bubbleTypes.setLayout(bubbleTypesLayout)
        mainLayout.addWidget(bubbleTypes)

        # Color de Relleno
        colorLayout = QHBoxLayout()
        self.bubbleColorButton = QPushButton(self)
        self.bubbleColor = QColor("white")
        self.updateButtonIcon(self.bubbleColorButton, self.bubbleColor)
        colorLayout.addWidget(QLabel("Fill Color:"))
        colorLayout.addWidget(self.bubbleColorButton)
        mainLayout.addLayout(colorLayout)

        # Configuración del Borde (Outline)
        outlineSize = QGroupBox("Outline")
        outlineLayout = QHBoxLayout()
        
        self.outlineSlider = QSlider(Qt.Horizontal)
        self.outlineSlider.setRange(0, 20)
        self.outlineSlider.setValue(3)
        
        self.outlineSpinBox = QSpinBox()
        self.outlineSpinBox.setRange(0, 20)
        self.outlineSpinBox.setValue(3)
        
        self.outlineColorButton = QPushButton(self)
        self.outlineColor = QColor("black")
        self.updateButtonIcon(self.outlineColorButton, self.outlineColor)
        
        outlineLayout.addWidget(self.outlineSlider)
        outlineLayout.addWidget(self.outlineSpinBox)
        outlineLayout.addWidget(self.outlineColorButton)
        outlineSize.setLayout(outlineLayout)
        mainLayout.addWidget(outlineSize)

        # Opacity controls (Text, Bubble, Outline)
        opacityGroup = QGroupBox("Opacity")
        opacityLayout = QVBoxLayout()

        # Text opacity
        textRow = QHBoxLayout()
        textRow.addWidget(QLabel("Text Opacity:"))
        self.textOpacitySlider = QSlider(Qt.Horizontal)
        self.textOpacitySlider.setRange(0, 100)
        self.textOpacitySlider.setValue(100)
        self.textOpacitySpin = QSpinBox()
        self.textOpacitySpin.setRange(0, 100)
        self.textOpacitySpin.setValue(100)
        textRow.addWidget(self.textOpacitySlider)
        textRow.addWidget(self.textOpacitySpin)
        opacityLayout.addLayout(textRow)

        # Bubble (background) opacity
        bubbleRow = QHBoxLayout()
        bubbleRow.addWidget(QLabel("Bubble Opacity:"))
        self.bubbleOpacitySlider = QSlider(Qt.Horizontal)
        self.bubbleOpacitySlider.setRange(0, 100)
        self.bubbleOpacitySlider.setValue(100)
        self.bubbleOpacitySpin = QSpinBox()
        self.bubbleOpacitySpin.setRange(0, 100)
        self.bubbleOpacitySpin.setValue(100)
        bubbleRow.addWidget(self.bubbleOpacitySlider)
        bubbleRow.addWidget(self.bubbleOpacitySpin)
        opacityLayout.addLayout(bubbleRow)

        # Outline opacity
        outlineRow2 = QHBoxLayout()
        outlineRow2.addWidget(QLabel("Outline Opacity:"))
        self.outlineOpacitySlider = QSlider(Qt.Horizontal)
        self.outlineOpacitySlider.setRange(0, 100)
        self.outlineOpacitySlider.setValue(100)
        self.outlineOpacitySpin = QSpinBox()
        self.outlineOpacitySpin.setRange(0, 100)
        self.outlineOpacitySpin.setValue(100)
        outlineRow2.addWidget(self.outlineOpacitySlider)
        outlineRow2.addWidget(self.outlineOpacitySpin)
        opacityLayout.addLayout(outlineRow2)

        opacityGroup.setLayout(opacityLayout)
        mainLayout.addWidget(opacityGroup)

        # Configuración de Texto
        speechGroup = QGroupBox("Text Settings")
        speechLayout = QVBoxLayout()
        
        fontRow = QHBoxLayout()
        self.speechFont = QFontComboBox()
        self.speechFontSize = QSpinBox()
        self.speechFontSize.setRange(5, 200)
        self.speechFontSize.setValue(14)
        
        self.fontColorButton = QPushButton()
        self.speechFontColor = QColor("black")
        self.updateButtonIcon(self.fontColorButton, self.speechFontColor)
        
        fontRow.addWidget(self.speechFont)
        fontRow.addWidget(self.speechFontSize)
        fontRow.addWidget(self.fontColorButton)
        speechLayout.addLayout(fontRow)

        self.bubbleText = QTextEdit("Hello Krita!")
        self.bubbleText.setMaximumHeight(80)
        speechLayout.addWidget(self.bubbleText)
        
        self.autocenter = QCheckBox("Auto-wrap Text")
        self.autocenter.setChecked(True)
        speechLayout.addWidget(self.autocenter)

        speechGroup.setLayout(speechLayout)
        mainLayout.addWidget(speechGroup)

        # Configuración de la Cola (Tail)
        tailGroup = QGroupBox("Tail Settings")
        tailLayout = QVBoxLayout()
        
        sizeLayout = QHBoxLayout()
        sizeLayout.addWidget(QLabel("Size:"))
        self.tailSlider = QSlider(Qt.Horizontal)
        self.tailSlider.setRange(0, 200)
        self.tailSlider.setValue(50)
        self.tailSpinBox = QSpinBox()
        self.tailSpinBox.setRange(0, 200)
        self.tailSpinBox.setValue(50)
        sizeLayout.addWidget(self.tailSlider)
        sizeLayout.addWidget(self.tailSpinBox)
        tailLayout.addLayout(sizeLayout)
        
        # Posiciones de la cola (1-9)
        self.tailPosGroup = QGroupBox("Position")
        posLayout = QHBoxLayout()
        self.tailRadios = []
        for i in range(9):
            rb = QRadioButton(str(i+1))
            if i == 6: rb.setChecked(True) # Default bottom-leftish
            self.tailRadios.append(rb)
            posLayout.addWidget(rb)
            rb.clicked.connect(self.updatePreview)
            
        self.tailPosGroup.setLayout(posLayout)
        tailLayout.addWidget(self.tailPosGroup)
        
        tailGroup.setLayout(tailLayout)
        mainLayout.addWidget(tailGroup)

        # --- CONNECTIONS ---
        self.addOnPage.clicked.connect(self.addOnPageShape)
        
        # Redraw triggers
        self.typeSquare.clicked.connect(self.updatePreview)
        self.typeSharpSquare.clicked.connect(self.updatePreview)
        self.typeRound.clicked.connect(self.updatePreview)
        self.typeCloud.clicked.connect(self.updatePreview)
        self.typeShout.clicked.connect(self.updatePreview)
        
        self.bubbleColorButton.clicked.connect(self.changeBubbleColor)
        self.outlineColorButton.clicked.connect(self.changeOutlineColor)
        self.fontColorButton.clicked.connect(self.changeFontColor)
        
        self.outlineSlider.valueChanged.connect(self.outlineSpinBox.setValue)
        self.outlineSpinBox.valueChanged.connect(self.outlineSlider.setValue)
        self.outlineSlider.valueChanged.connect(self.updatePreview)
        
        self.tailSlider.valueChanged.connect(self.tailSpinBox.setValue)
        self.tailSpinBox.valueChanged.connect(self.tailSlider.setValue)
        self.tailSlider.valueChanged.connect(self.updatePreview)
        
        self.bubbleText.textChanged.connect(self.updatePreview)
        self.speechFont.currentFontChanged.connect(self.updatePreview)
        self.speechFontSize.valueChanged.connect(self.updatePreview)
        # Opacity controls signals
        self.textOpacitySlider.valueChanged.connect(self.textOpacitySpin.setValue)
        self.textOpacitySpin.valueChanged.connect(self.textOpacitySlider.setValue)
        self.textOpacitySlider.valueChanged.connect(self.updatePreview)

        self.bubbleOpacitySlider.valueChanged.connect(self.bubbleOpacitySpin.setValue)
        self.bubbleOpacitySpin.valueChanged.connect(self.bubbleOpacitySlider.setValue)
        self.bubbleOpacitySlider.valueChanged.connect(self.updatePreview)

        self.outlineOpacitySlider.valueChanged.connect(self.outlineOpacitySpin.setValue)
        self.outlineOpacitySpin.valueChanged.connect(self.outlineOpacitySlider.setValue)
        self.outlineOpacitySlider.valueChanged.connect(self.updatePreview)
        
        # --- SCROLL AREA SETUP ---
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(mainLayout)
        self.scrollArea.setWidget(container)
        self.setWidget(self.scrollArea)
        
        self.updatePreview()

    # --- HELPER FUNCTIONS ---

    def canvasChanged(self, canvas):
            pass
    # ------------------------

    def updateButtonIcon(self, button, color):
        pixmap = QPixmap(32, 32)
        pixmap.fill(color)
        button.setIcon(QIcon(pixmap))

    def changeBubbleColor(self):
        c = QColorDialog.getColor(self.bubbleColor)
        if c.isValid():
            self.bubbleColor = c
            self.updateButtonIcon(self.bubbleColorButton, c)
            self.updatePreview()

    def changeOutlineColor(self):
        c = QColorDialog.getColor(self.outlineColor)
        if c.isValid():
            self.outlineColor = c
            self.updateButtonIcon(self.outlineColorButton, c)
            self.updatePreview()

    def changeFontColor(self):
        c = QColorDialog.getColor(self.speechFontColor)
        if c.isValid():
            self.speechFontColor = c
            self.updateButtonIcon(self.fontColorButton, c)
            self.updatePreview()

    def getFormattedTextLines(self):
        # Lógica simplificada para envolver texto
        text = self.bubbleText.toPlainText()
        if not text: return [""]
        
        if not self.autocenter.isChecked():
            return text.split('\n')
            
        # Estimación básica de caracteres por línea basada en la raíz cuadrada de la longitud
        # para intentar mantener una forma cuadrada/redonda
        target_chars = int(math.sqrt(len(text)) * 2.5)
        if target_chars < 5: target_chars = 5
        
        words = text.split()
        lines = []
        current_line = []
        current_len = 0
        
        for word in words:
            if current_len + len(word) > target_chars and current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_len = len(word)
            else:
                current_line.append(word)
                current_len += len(word) + 1
        if current_line:
            lines.append(" ".join(current_line))
            
        return lines

    # --- MATH & GEOMETRY GENERATION ---

    def generate_svg(self):
        # 1. Calcular dimensiones del texto
        lines = self.getFormattedTextLines()
        font = self.speechFont.currentFont()
        font_size = self.speechFontSize.value()
        font.setPixelSize(font_size)
        metrics = QFontMetrics(font)
        
        line_height = metrics.height()
        text_width = 0
        for line in lines:
            w = metrics.width(line)
            if w > text_width: text_width = w
            
        text_height = line_height * len(lines)
        
        padding = font_size * 2 # Espacio interior
        
        # Dimensiones del cuerpo de la burbuja
        body_w = text_width + padding
        body_h = text_height + padding
        
        # Ajustes extra para nube y grito para que el texto no se salga
        if self.typeShout.isChecked():
            body_w *= 1.4
            body_h *= 1.4
        elif self.typeCloud.isChecked():
            body_w *= 1.2
            body_h *= 1.2

        cx = body_w / 2
        cy = body_h / 2
        
        # Margen del canvas SVG para permitir que la cola se salga
        tail_len = self.tailSlider.value()
        margin = tail_len + 50 
        canvas_w = body_w + (margin * 2)
        canvas_h = body_h + (margin * 2)
        
        offset_x = margin
        offset_y = margin

        # 2. Generar Path de la Burbuja (Body)
        path_d = ""
        
        if self.typeSquare.isChecked():
            # Rectángulo con esquinas redondeadas
            r = 15 # radio de esquina
            path_d = f"M {offset_x + r},{offset_y} " \
                     f"L {offset_x + body_w - r},{offset_y} Q {offset_x + body_w},{offset_y} {offset_x + body_w},{offset_y + r} " \
                     f"L {offset_x + body_w},{offset_y + body_h - r} Q {offset_x + body_w},{offset_y + body_h} {offset_x + body_w - r},{offset_y + body_h} " \
                     f"L {offset_x + r},{offset_y + body_h} Q {offset_x},{offset_y + body_h} {offset_x},{offset_y + body_h - r} " \
                     f"L {offset_x},{offset_y + r} Q {offset_x},{offset_y} {offset_x + r},{offset_y} Z"

        elif self.typeSharpSquare.isChecked():
            # Cuadrado perfecto (Sharp)
            cx_abs = offset_x + body_w/2
            cy_abs = offset_y + body_h/2
            path_d = f"M {offset_x},{offset_y} " \
                     f"L {offset_x + body_w},{offset_y} " \
                     f"L {offset_x + body_w},{offset_y + body_h} " \
                     f"L {offset_x},{offset_y + body_h} Z"

        elif self.typeRound.isChecked():
            # Elipse perfecta usando comandos de arco SVG
            rx = body_w / 2
            ry = body_h / 2
            cx_abs = offset_x + rx
            cy_abs = offset_y + ry
            path_d = f"M {cx_abs - rx},{cy_abs} " \
                     f"a {rx},{ry} 0 1,0 {rx * 2},0 " \
                     f"a {rx},{ry} 0 1,0 -{rx * 2},0 Z"

        elif self.typeCloud.isChecked():
            # Nube generada por arcos superpuestos
            rx = body_w / 2
            ry = body_h / 2
            cx_abs = offset_x + rx
            cy_abs = offset_y + ry
            
            # Generar 8 puntos alrededor de la elipse y crear arcos
            path_d = f"M {cx_abs + rx},{cy_abs} "
            for i in range(1, 9):
                angle = (i / 8) * 2 * math.pi
                px = cx_abs + math.cos(angle) * rx
                py = cy_abs + math.sin(angle) * ry
                
                # Puntos de control para que sea "fluffy"
                prev_angle = ((i-1) / 8) * 2 * math.pi
                mid_angle = (prev_angle + angle) / 2
                
                # El "bulto" de la nube sale hacia afuera
                bulge = 1.4 # Qué tan grandes son los bultos
                ctrl_x = cx_abs + math.cos(mid_angle) * (rx * bulge)
                ctrl_y = cy_abs + math.sin(mid_angle) * (ry * bulge)
                
                path_d += f"Q {ctrl_x},{ctrl_y} {px},{py} "
            path_d += "Z"

        elif self.typeShout.isChecked():
            # Grito / Picos (Spiky)
            rx = body_w / 2
            ry = body_h / 2
            cx_abs = offset_x + rx
            cy_abs = offset_y + ry
            
            points = []
            num_spikes = 24
            for i in range(num_spikes * 2):
                angle = (i / (num_spikes * 2)) * 2 * math.pi
                
                # Alternar entre radio interno y externo
                is_tip = (i % 2 != 0)
                
                # Variación pseudo-aleatoria basada en seno para que no sea demasiado uniforme
                wobble = math.sin(i * 3) * 0.1 
                
                current_r_x = rx * (1.1 + wobble if is_tip else 0.8)
                current_r_y = ry * (1.1 + wobble if is_tip else 0.8)
                
                px = cx_abs + math.cos(angle) * current_r_x
                py = cy_abs + math.sin(angle) * current_r_y
                points.append(f"{px},{py}")
            
            path_d = "M " + " L ".join(points) + " Z"

        # 3. Generar la Cola (Tail)
        tail_svg = ""
        
        # Determinar posición de la cola (1-8 mapeado a ángulos)
        active_pos_idx = 0
        for i, rb in enumerate(self.tailRadios):
            if rb.isChecked():
                active_pos_idx = i
                break
        
        # Mapeo de índices 0-8 a vectores dirección (aprox)
        # 0: TL, 1: T, 2: TR, 3: R, 4: BR, 5: B, 6: BL, 7: L, 8: B-mirror
        # Ángulos en radianes (ajustados visualmente)
        angles = [
            -3*math.pi/4, -math.pi/2, -math.pi/4, # Arriba (1, 2, 3)
            0,                                    # Derecha (4)
            math.pi/4, math.pi/2, 3*math.pi/4,    # Abajo (5, 6, 7)
            math.pi,                              # Izquierda (8)
            math.pi/2                             # Abajo Espejo (9)
        ]
        tail_angle = angles[active_pos_idx]
        
        cx_abs = offset_x + body_w/2
        cy_abs = offset_y + body_h/2

        # Opacity values (0.0 - 1.0)
        try:
            bubble_opacity = self.bubbleOpacitySlider.value() / 100.0
            outline_opacity = self.outlineOpacitySlider.value() / 100.0
            text_opacity = self.textOpacitySlider.value() / 100.0
        except Exception:
            bubble_opacity = 1.0
            outline_opacity = 1.0
            text_opacity = 1.0
        
        # Punto de origen en el borde de la burbuja (simplificado como círculo por ahora)
        # Para mejorar, se proyecta desde el centro hasta el radio
        start_x = cx_abs + math.cos(tail_angle) * (body_w/2.2) 
        start_y = cy_abs + math.sin(tail_angle) * (body_h/2.2)
        
        # Punto final de la cola (punta)
        tip_x = start_x + math.cos(tail_angle) * tail_len
        tip_y = start_y + math.sin(tail_angle) * tail_len
        
        if tail_len > 0:
            if self.typeCloud.isChecked():
                # Cola de pensamiento (Círculos pequeños)
                # Dibujamos 3 círculos disminuyendo de tamaño hacia la punta
                for k in range(3):
                    ratio = (k + 1) / 4.0
                    bub_x = start_x + (tip_x - start_x) * ratio
                    bub_y = start_y + (tip_y - start_y) * ratio
                    bub_r = (font_size / 2) * (1 - ratio + 0.2)
                    tail_svg += f'<circle cx="{bub_x}" cy="{bub_y}" r="{bub_r}" fill="{self.bubbleColor.name()}" fill-opacity="{bubble_opacity}" stroke="{self.outlineColor.name()}" stroke-opacity="{outline_opacity}" stroke-width="{self.outlineSpinBox.value()}"/>'
            else:
                # Cola estándar (Grito, Redonda, Cuadrada)
                # Calculamos base de la cola perpendicular al ángulo
                base_w = font_size * 1.5
                perp_angle = tail_angle + math.pi/2
                
                p1_x = start_x + math.cos(perp_angle) * (base_w/2)
                p1_y = start_y + math.sin(perp_angle) * (base_w/2)
                
                p2_x = start_x - math.cos(perp_angle) * (base_w/2)
                p2_y = start_y - math.sin(perp_angle) * (base_w/2)
                
                # Curvatura (Estilo Bézier)
                # El punto de control curva la cola ligeramente
                mid_x = (start_x + tip_x) / 2
                mid_y = (start_y + tip_y) / 2
                
                # Determinar dirección de la curva basada en el índice (par/impar para variar izquierda/derecha)
                curve_strength = tail_len * 0.3
                if active_pos_idx % 2 == 0:
                    ctrl_x = mid_x + math.cos(perp_angle) * curve_strength
                    ctrl_y = mid_y + math.sin(perp_angle) * curve_strength
                else:
                    ctrl_x = mid_x - math.cos(perp_angle) * curve_strength
                    ctrl_y = mid_y - math.sin(perp_angle) * curve_strength
                
                # Dibujamos la cola como un path cerrado
                # Q = Quadratic Bezier
                tail_d = f"M {p1_x},{p1_y} Q {ctrl_x},{ctrl_y} {tip_x},{tip_y} Q {ctrl_x},{ctrl_y} {p2_x},{p2_y} Z"
                
                # Fusionar visualmente: Dibujar la cola ANTES del path principal si es SVG plano, 
                # o dibujarlo del mismo color.
                # Aquí simplemente añadimos el path de la cola.
                tail_svg = f'<path d="{tail_d}" fill="{self.bubbleColor.name()}" fill-opacity="{bubble_opacity}" stroke="{self.outlineColor.name()}" stroke-opacity="{outline_opacity}" stroke-width="{self.outlineSpinBox.value()}" stroke-linejoin="round"/>'

        # 4. Construir SVG Final
        style_main = f'fill="{self.bubbleColor.name()}" fill-opacity="{bubble_opacity}" stroke="{self.outlineColor.name()}" stroke-opacity="{outline_opacity}" stroke-width="{self.outlineSpinBox.value()}" stroke-linejoin="round"'
        
        # Si es nube, la cola va separada (círculos). Si no, intentamos unificar visualmente
        svg_content = ""
        
        # Orden de dibujado: Cola primero, luego cuerpo (para ocultar la unión de la cola)
        if not self.typeCloud.isChecked():
            svg_content += tail_svg
            
        svg_content += f'<path d="{path_d}" {style_main} />'
        
        if self.typeCloud.isChecked():
            svg_content += tail_svg # En nube, las bolitas van encima o aparte

        # 5. Añadir Texto
        text_svg = ""
        font_family = font.family()
        text_fill = self.speechFontColor.name()
        
        # Calculamos la altura total que ocupa el bloque de texto
        total_text_height = line_height * len(lines)

        # Fórmula: Centro de la burbuja (cy_abs) - Mitad del bloque de texto + Corrección visual de la primera línea
        # (line_height * 0.75 ayuda a alinear la base de la fuente visualmente al centro)
        start_y = cy_abs - (total_text_height / 2) + (line_height * 0.75)

        current_text_y = start_y
        
        for line in lines:
            # Centrar texto horizontalmente
            line_w = metrics.width(line)
            line_x = cx_abs 
            
            text_svg += f'<text x="{line_x}" y="{current_text_y}" font-family="{font_family}" font-size="{font_size}" fill="{text_fill}" fill-opacity="{text_opacity}" text-anchor="middle">{line}</text>'
            current_text_y += line_height

        final_svg = f'<svg width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg">' \
                    f'{svg_content}' \
                    f'{text_svg}' \
                    f'</svg>'
                    
        return final_svg

    def updatePreview(self):
        svg_code = self.generate_svg()
        self.preview.renderer().load(bytearray(svg_code, encoding='utf-8'))

    def addOnPageShape(self):
        svg_code = self.generate_svg()
        
        doc = Krita.instance().activeDocument()
        if doc:
            root = doc.rootNode()
            layer_name = "Bubble"
            if self.typeShout.isChecked(): layer_name = "Shout"
            elif self.typeCloud.isChecked(): layer_name = "Thought"
                
            new_layer = doc.createVectorLayer(layer_name)
            root.addChildNode(new_layer, None)
            
            # Krita necesita el SVG en formato correcto
            new_layer.addShapesFromSvg(svg_code)
            doc.refreshProjection()


Krita.instance().addDockWidgetFactory(DockWidgetFactory("Rogudator's Speech Bubble Generator V2", DockWidgetFactoryBase.DockRight, RSBGDocker))
