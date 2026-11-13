package com.offbynull.diagramhelper;

import static com.google.common.base.Throwables.getStackTraceAsString;
import com.google.common.hash.Hashing;
import java.awt.Dimension;
import java.awt.FontMetrics;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Line2D;
import java.awt.geom.NoninvertibleTransformException;
import java.awt.geom.Rectangle2D;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import static java.lang.Math.abs;
import static java.lang.Math.max;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.ArrayList;
import java.util.List;
import static java.util.Locale.ENGLISH;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import org.apache.batik.anim.dom.SAXSVGDocumentFactory;
import org.apache.batik.bridge.BridgeContext;
import org.apache.batik.bridge.DocumentLoader;
import org.apache.batik.bridge.GVTBuilder;
import org.apache.batik.bridge.UserAgent;
import org.apache.batik.bridge.UserAgentAdapter;
import org.apache.batik.dom.GenericDOMImplementation;
import org.apache.batik.gvt.GraphicsNode;
import org.apache.batik.svggen.SVGGeneratorContext;
import org.apache.batik.svggen.SVGGraphics2D;
import org.apache.batik.util.XMLResourceDescriptor;
import org.w3c.dom.DOMImplementation;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class MainNumberLineDraw {

    public static void main(String[] args) throws IOException, NoninvertibleTransformException {
        try (Writer mdOut = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            try {
                String input = Files.readString(Path.of("/input/input.data"), UTF_8).trim();
                
                double width = 400;
                List<LineNotch> notches = new ArrayList<>();
                
                Scanner scanner = new Scanner(input);
                while (scanner.hasNext()) {
                    String token = scanner.next();
                    switch (token) {
                        case "width":
                            width = scanner.nextDouble();
                            break;
                        case "-":
                            notches.add(new LineNotch(scanner.nextDouble(), NotchType.IGNORE));
                            break;
                        case "|":
                            notches.add(new LineNotch(scanner.nextDouble(), NotchType.LINE));
                            break;
                        case "*":
                            notches.add(new LineNotch(scanner.nextDouble(), NotchType.CIRCLE));
                            break;
                        default:
                            throw new IllegalArgumentException("Bad token " + token);
                    }
                }

                DOMImplementation domImpl = GenericDOMImplementation.getDOMImplementation();
                Document document = domImpl.createDocument("http://www.w3.org/2000/svg", "svg", null);

                SVGGraphics2D g = new SVGGraphics2D(SVGGeneratorContext.createDefault(document), true);

                drawNumberLine(g, width, notches);

                String outputFileName = MainNumberLineDraw.class.getSimpleName()
                        + Hashing.murmur3_128(32).hashString(input, UTF_8).toString() + ".svg";
                writeSvg(g, Path.of("/output", outputFileName));
                mdOut.write("![Concept diagram for line number " + notches.stream().map(n -> n.x).map(DECIMAL_FORMAT::format).collect(joining(" ")) + "](" + outputFileName + ")");
            } catch (Exception e) {
                mdOut.append("`{bm-disable-all}`\n\n");
                mdOut.append(getStackTraceAsString(e));
                mdOut.append("`{bm-enable-all}`");
            }
        }

//        DOMImplementation domImpl = GenericDOMImplementation.getDOMImplementation();
//        Document document = domImpl.createDocument("http://www.w3.org/2000/svg", "svg", null);
//
//        int width = 400;
//        int height = 400;
//
//        SVGGraphics2D g = new SVGGraphics2D(SVGGeneratorContext.createDefault(document), true);
//
//        drawNumberLine(g, width, List.of(new LineNotch(0, NotchType.LINE), new LineNotch(5, NotchType.LINE)));
//
//        writeSvg(g, Path.of("test.svg"));
//        Desktop.getDesktop().open(new File("test.svg"));
    }
    
    public static void drawNumberLine(SVGGraphics2D g, double outputWidth, List<LineNotch> points) throws NoninvertibleTransformException {;
        double minPoint = points.stream().mapToDouble(p -> p.x).min().orElse(Double.NaN);
        double maxPoint = points.stream().mapToDouble(p -> p.x).max().orElse(Double.NaN);
        double extent = max(abs(minPoint), abs(maxPoint));
        double[] outputPoints = points.stream().mapToDouble(p -> p.x)
                .map(p -> p / extent) // scale it between -1 and 1
                .map(p -> (p + 1) / 2) // scale it between 0 and 1
                .map(p -> p * outputWidth) // scale it between 0 and outputWidth
                .toArray();

        g.draw(new Line2D.Double(0, 0, outputWidth, 0));

        for (int i = 0; i < points.size(); i++) {
            LineNotch point = points.get(i);
            double outputPoint = outputPoints[i];
            ;
            drawNotch(g, point, outputPoint, 0);
        }
    }

    private static final DecimalFormat DECIMAL_FORMAT;

    static {
        DECIMAL_FORMAT = new DecimalFormat("0", DecimalFormatSymbols.getInstance(ENGLISH));
        DECIMAL_FORMAT.setMaximumFractionDigits(340);
    }

    private static void drawNotch(SVGGraphics2D g, LineNotch notch, double x, double y) throws NoninvertibleTransformException {
        String str = DECIMAL_FORMAT.format(notch.x);
        FontMetrics fm = g.getFontMetrics();
        double width = fm.stringWidth(str);
        double height = fm.getHeight();

        switch (notch.type) {
            case IGNORE:
                break;
            case LINE:
                g.draw(new Line2D.Double(x, 0, x, 5));
                g.drawString(str, (float) (x - width / 2), (float) (y + height + 5));
                break;
            case CIRCLE:
                g.fill(new Ellipse2D.Double(x-5, -5, 10, 10));
                g.drawString(str, (float) (x - width / 2), (float) (y + height + 5));
                break;
            default:
                throw new IllegalStateException();
        }
    }

    public static final class LineNotch {

        public final double x;
        public final NotchType type;

        public LineNotch(double x, NotchType notchType) {
            this.x = x;
            this.type = notchType;
        }
    }

    public enum NotchType {
        IGNORE,
        LINE,
        CIRCLE
    }
    
    
    
    
    
    
    
    
    

    private static void writeSvg(SVGGraphics2D g, Path path) throws IOException {
        // after any invocation to stream() or any dom accessor (including this method), g's contents will clear and you'll need to reset it
          // see https://issues.apache.org/jira/browse/BATIK-555
          // see http://batik.2283329.n4.nabble.com/How-to-set-viewbox-attribute-in-SVGGraphics2D-td2979195.html
        Element tlgElement = g.getTopLevelGroup();
        g.setTopLevelGroup(tlgElement);
        
        // write out
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        OutputStreamWriter writer = new OutputStreamWriter(baos, UTF_8);
        g.stream(writer, false);
        g.setTopLevelGroup(tlgElement); // bug work around, see above
        
        // load back up and get svg bounds
        SAXSVGDocumentFactory factory = new SAXSVGDocumentFactory(XMLResourceDescriptor.getXMLParserClassName());
        Document document = factory.createDocument(
                null,
                new ByteArrayInputStream(baos.toByteArray())
        );
        UserAgent userAgent = new UserAgentAdapter();
        DocumentLoader documentLoader = new DocumentLoader(userAgent);
        BridgeContext bridgeContext = new BridgeContext(userAgent, documentLoader);
        bridgeContext.setDynamic(true);
        GraphicsNode graphicsNode = new GVTBuilder().build(bridgeContext, document);
        Rectangle2D bounds = graphicsNode.getSensitiveBounds();

        
        // pull out element to set viewport and bounds (dont use g.setSVGCanvasSize because it requires ints instead of doubles) and write out
        Element root = g.getRoot();
        root.setAttributeNS(null, "viewBox", bounds.getMinX() + " " + bounds.getMinY() + " " + bounds.getWidth()+ " " + bounds.getHeight());
        root.setAttributeNS(null, "width",  "" + bounds.getWidth());
        root.setAttributeNS(null, "height", "" + bounds.getHeight());
        try (Writer fileWriter = Files.newBufferedWriter(path)) {
            g.stream(root, fileWriter, false, false); // stream out the root element specifically -- g is cleared so if we stream it out directly it'll be blank
        }
        g.setTopLevelGroup(tlgElement); // bug work around, see above
    }
}
