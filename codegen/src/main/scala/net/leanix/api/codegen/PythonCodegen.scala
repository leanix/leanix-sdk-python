/*
 * The MIT License (MIT)	 
 *
 * Copyright (c) 2014 LeanIX GmbH
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

package net.leanix.api.codegen

import java.io.File
import com.wordnik.swagger.codegen.BasicPythonGenerator

object PythonCodegen extends BasicPythonGenerator {
  def main(args: Array[String]) = generateClient(args)

  // location of templates
  override def templateDir = "swagger/python"

  def destinationRoot = "target/generated-sources/swagger"
  
  override def destinationDir = destinationRoot + "/src/main/python/leanix"

  // supporting classes
  override def supportingFiles =
    List(
    ("__init__.mustache", destinationDir, "__init__.py"),
    ("swagger.mustache", destinationDir + File.separator + apiPackage.getOrElse(""), "swagger.py"),
    ("__init__.mustache", destinationDir + File.separator + modelPackage.getOrElse(""), "__init__.py")
		)
}
