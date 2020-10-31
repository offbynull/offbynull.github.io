package com.offbynull.diagramhelper;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import com.google.common.hash.Hashing;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.geom.AffineTransform;
import java.awt.geom.Arc2D;
import java.awt.geom.Rectangle2D;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;
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
import org.w3c.dom.*;

public final class MainFractionDraw {

    public static void main(String[] args) throws IOException {
        try (Writer mdOut = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            try {
                String input = Files.readString(Path.of("/input/input.data"), UTF_8).trim();
                
                int diameter = 500;
                Scanner scanner = new Scanner(input);
                if (scanner.hasNext("radius")) {
                    scanner.next();
                    diameter = scanner.nextInt();
                }
                
                int numerator = scanner.nextInt();
                int denominator = scanner.nextInt();
                
                Preconditions.checkArgument(numerator >= 0, "For the purposes of this tool, fraction must be positive");
                Preconditions.checkArgument(denominator >= 0, "For the purposes of this tool, fraction must be positive");
                Preconditions.checkArgument(denominator != 0, "Denominator can't be 0");
                
                DOMImplementation domImpl = GenericDOMImplementation.getDOMImplementation();
                Document document = domImpl.createDocument("http://www.w3.org/2000/svg", "svg", null);

                SVGGraphics2D g = new SVGGraphics2D(SVGGeneratorContext.createDefault(document), true);
                g.setStroke(new BasicStroke(0.2f));

                
                double degreeOffset = 90;
                double degreesPerSlice = 360.0 / denominator;
                if (numerator == 0) {
                        drawSlices(g, diameter, diameter, 0, denominator, degreesPerSlice, degreeOffset);
                } else {
                    int it = 0;
                    while (numerator > 0) {
                        int consumed = Math.min(numerator, denominator);
                        numerator -= consumed;

                        double xOffset = (it * diameter) + (it * diameter * 0.1);
                        AffineTransform t = new AffineTransform();
                        t.translate(xOffset, 0.0);
                        g.setTransform(t);

                        drawSlices(g, diameter, diameter, consumed, denominator, degreesPerSlice, degreeOffset);
                        it++;
                    }
                }

                String outputFileName = MainNumberLineDraw.class.getSimpleName()
                        + Hashing.murmur3_128(32).hashString(input, UTF_8).toString() + ".svg";
                writeSvg(g, Path.of("/output", outputFileName));
                mdOut.write("![Concept diagram for fraction " + numerator + " / " + denominator + "](" + outputFileName + ")");
            } catch (Exception e) {
                mdOut.append("`{bm-disable-all}`\n\n");
                mdOut.append(getStackTraceAsString(e));
                mdOut.append("`{bm-enable-all}`");
            }
        }
    }
    
    private static void drawSlices(SVGGraphics2D g, double width, double height, int fillSlices, int maxSlices, double degreesPerSlice, double degreeOffset) {
        g.setPaint(Color.gray);
        for (int i = 0; i < fillSlices; i++) {
            g.fill(
                    new Arc2D.Double(
                            0,
                            0,
                            width,
                            height,
                            degreeOffset + (i * degreesPerSlice),
                            degreesPerSlice,
                            Arc2D.PIE
                    )
            );
        }
        g.setPaint(Color.white);
        for (int i = fillSlices; i < maxSlices; i++) {
            g.fill(
                    new Arc2D.Double(
                            0,
                            0,
                            width,
                            height,
                            degreeOffset + (i * degreesPerSlice),
                            degreesPerSlice,
                            Arc2D.PIE
                    )
            );
        }
        g.setPaint(Color.black);
        for (int i = 0; i < maxSlices; i++) {
            g.draw(
                    new Arc2D.Double(
                            0,
                            0,
                            width,
                            height,
                            degreeOffset + (i * degreesPerSlice),
                            degreesPerSlice,
                            Arc2D.PIE
                    )
            );
        }
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